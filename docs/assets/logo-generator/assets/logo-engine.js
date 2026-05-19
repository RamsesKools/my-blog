/* logo-engine.js — shared SVG generation function for logo-generator
   Used by both logo-generator.html (browser) and generate-logos.js (Node CLI).
   No dependencies. Pure function: params in, SVG string out.
*/

const VERSION = '1.0.0';

/**
 * @typedef {Object} LogoParams
 * @property {string}  [color='#3E77DC']         Primary color (hex)
 * @property {string}  [color_bg='transparent']  Background color
 * @property {number}  [left_width=100]
 * @property {number}  [left_height=100]
 * @property {number}  [right_width=100]
 * @property {number}  [right_height=100]
 * @property {number}  [gap=0]
 * @property {number}  [corner_radius=4]
 * @property {number}  [stroke_width=3]
 * @property {string}  [left_text='R']
 * @property {string}  [right_text='K']
 * @property {string}  [font_family='Geist']
 * @property {number}  [font_size_ratio=0.55]     Font size as fraction of square height
 * @property {number}  [font_weight=600]
 * @property {string}  [left_mode='filled_cutout']        filled_cutout | filled_letter | outline
 * @property {string}  [right_mode='outline_filled_letter'] outline_filled_letter | filled_cutout | filled
 * @property {boolean} [continuous_rounding=false]   Zero the inner touching corners, keep outer corners rounded
 * @property {string}  [left_text_align='center']  Horizontal text alignment in left square: center | left | right
 * @property {string}  [right_text_align='center'] Horizontal text alignment in right square: center | left | right
 * @property {string}  [left_valign='middle']       Vertical alignment of left square: top | middle | bottom
 * @property {string}  [right_valign='middle']      Vertical alignment of right square: top | middle | bottom
 * @property {number}  [text_padding=0.3]           Padding between text and box edge, as fraction of font size (0 = flush)
 * @property {string}  [filename='logo']            Used in <title> and <desc>
 * @property {string}  [font_embed]                 Base64-encoded woff2 font data to embed in SVG (CLI only)
 */

/**
 * Generate an SVG string from logo parameters.
 * @param {LogoParams} params
 * @returns {string} SVG markup
 */
function generateLogoSVG(params) {
    const p = Object.assign({
        color: '#3E77DC',
        color_bg: 'transparent',
        left_width: 100,
        left_height: 100,
        right_width: 100,
        right_height: 100,
        gap: 0,
        corner_radius: 4,
        stroke_width: 3,
        left_text: 'R',
        right_text: 'K',
        font_family: 'Geist',
        font_size_ratio: 0.55,
        font_weight: 600,
        left_mode: 'filled_cutout',
        right_mode: 'outline_filled_letter',
        continuous_rounding: false,
        left_text_align: 'center',
        right_text_align: 'center',
        left_valign: 'middle',
        right_valign: 'middle',
        text_padding: 0.3,
        box_offset: 0,
        transparent_outside: false,
        filename: 'logo',
    }, params);

    const lw = Number(p.left_width);
    const lh = Number(p.left_height);
    const rw = Number(p.right_width);
    const rh = Number(p.right_height);
    const gap = Number(p.gap);
    const cr = Number(p.corner_radius);
    const sw = Number(p.stroke_width);
    const fsr = Number(p.font_size_ratio);
    const fw = Number(p.font_weight);
    const contRound = p.continuous_rounding === true || p.continuous_rounding === 'true';
    const textPadding = Number(p.text_padding);
    const boxOffset = Number(p.box_offset);

    // box_offset > 0: left box shifts down; box_offset < 0: right box shifts down
    const ly = Math.max(0,  boxOffset);
    const ry = Math.max(0, -boxOffset);

    const totalWidth  = lw + gap + rw;
    const totalHeight = Math.max(ly + lh, ry + rh);

    const leftFontSize  = lh * fsr;
    const rightFontSize = rh * fsr;

    // Resolve SVG text-anchor and x position for a square given alignment
    function textPos(squareX, squareW, fontSize, align) {
        const padding = fontSize * textPadding;
        if (align === 'left')  return { anchor: 'start',  x: squareX + padding };
        if (align === 'right') return { anchor: 'end',    x: squareX + squareW - padding };
        return                        { anchor: 'middle', x: squareX + squareW / 2 };
    }

    // Resolve vertical y of text centre within its square, given valign
    function textCY(squareY, squareH, fontSize, valign) {
        const padding = fontSize * textPadding;
        if (valign === 'top')    return squareY + padding + fontSize / 2;
        if (valign === 'bottom') return squareY + squareH - padding - fontSize / 2;
        return squareY + squareH / 2;
    }

    const lcy = textCY(ly, lh, leftFontSize,  p.left_valign);
    const rcy = textCY(ry, rh, rightFontSize, p.right_valign);

    const rxl = Math.min(cr, lw / 2, lh / 2);
    const rxr = Math.min(cr, rw / 2, rh / 2);

    // Right square x offset
    const rx = lw + gap;
    // Overlap: extend left box by 0.5px when gap=0 to prevent anti-aliasing seam.
    // The right box draws on top, hiding the overlap.
    const lrw = gap === 0 ? lw + 0.5 : lw;

    /**
     * Build an SVG path for a rectangle with per-corner radii.
     * corners: { tl, tr, br, bl } — each a radius value.
     */
    function roundedRect(x, y, w, h, { tl, tr, br, bl }) {
        return [
            `M ${x + tl} ${y}`,
            `H ${x + w - tr}`,
            tr ? `A ${tr} ${tr} 0 0 1 ${x + w} ${y + tr}` : '',
            `V ${y + h - br}`,
            br ? `A ${br} ${br} 0 0 1 ${x + w - br} ${y + h}` : '',
            `H ${x + bl}`,
            bl ? `A ${bl} ${bl} 0 0 1 ${x} ${y + h - bl}` : '',
            `V ${y + tl}`,
            tl ? `A ${tl} ${tl} 0 0 1 ${x + tl} ${y}` : '',
            'Z',
        ].filter(Boolean).join(' ');
    }

    // Corner radii for each square under continuous_rounding:
    // Without offset: left rounds tl/bl (outer), squares tr/br (inner touching).
    // With offset: inner corners that stick out beyond the other box are also rounded.
    if (contRound) {
        // A corner is "sticking out" if it sits beyond the other box's vertical extent.
        // Left inner-top (tr) sticks out if the left box starts above the right box.
        const lTopSticks    = ly < ry;   // left top is higher than right top
        const lBottomSticks = (ly + lh) > (ry + rh); // left bottom is lower than right bottom
        const rTopSticks    = ry < ly;
        const rBottomSticks = (ry + rh) > (ly + lh);

        var leftCorners  = { tl: rxl, tr: lTopSticks    ? rxl : 0, br: lBottomSticks ? rxl : 0, bl: rxl };
        var rightCorners = { tl: rTopSticks    ? rxr : 0, tr: rxr, br: rxr, bl: rBottomSticks ? rxr : 0 };
    } else {
        var leftCorners  = { tl: rxl, tr: rxl, br: rxl, bl: rxl };
        var rightCorners = { tl: rxr, tr: rxr, br: rxr, bl: rxr };
    }

    // Helper: shape string for a square (filled rect or path)
    function squarePath(x, y, w, h, corners) {
        const allSame = corners.tl === corners.tr && corners.tr === corners.br && corners.br === corners.bl;
        if (allSame) return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${corners.tl}"`;
        return `<path d="${roundedRect(x, y, w, h, corners)}"`;
    }

    // Helper: outline as a filled compound path (outer - inner, evenodd).
    // The outer edge always has the original corner radii, so it matches filled boxes.
    function outlinePath(x, y, w, h, corners, strokeW) {
        const outer = roundedRect(x, y, w, h, corners);
        const ic = {
            tl: Math.max(0, corners.tl - strokeW),
            tr: Math.max(0, corners.tr - strokeW),
            br: Math.max(0, corners.br - strokeW),
            bl: Math.max(0, corners.bl - strokeW),
        };
        const inner = roundedRect(x + strokeW, y + strokeW, w - 2 * strokeW, h - 2 * strokeW, ic);
        return `<path d="${outer} ${inner}" fill-rule="evenodd"`;
    }

    let defs = '';
    let shapes = '';

    // ---- LEFT SQUARE ----
    if (p.left_mode === 'filled_cutout') {
        const tp = textPos(0, lw, leftFontSize, p.left_text_align);
        const maskShape = squarePath(0, ly, lrw, lh, leftCorners);
        defs += `
    <mask id="mask-left">
      ${maskShape} fill="white"/>
      ${p.left_text ? `<text fill="black" text-anchor="${tp.anchor}" dominant-baseline="central"
            x="${tp.x}" y="${lcy}"
            font-size="${leftFontSize}" font-family="${esc(p.font_family)}, sans-serif"
            font-weight="${fw}">${esc(p.left_text)}</text>` : ''}
    </mask>`;
        const s = squarePath(0, ly, lrw, lh, leftCorners);
        shapes += `
    ${s} fill="${esc(p.color)}" mask="url(#mask-left)"/>`;

    } else if (p.left_mode === 'filled_letter') {
        const tp = textPos(0, lw, leftFontSize, p.left_text_align);
        const s = squarePath(0, ly, lrw, lh, leftCorners);
        shapes += `
    ${s} fill="${esc(p.color)}"/>`;
        if (p.left_text) {
            shapes += `
    <text fill="${esc(p.color_bg === 'transparent' ? '#ffffff' : p.color_bg)}" text-anchor="${tp.anchor}" dominant-baseline="central"
          x="${tp.x}" y="${lcy}"
          font-size="${leftFontSize}" font-family="${esc(p.font_family)}, sans-serif"
          font-weight="${fw}">${esc(p.left_text)}</text>`;
        }

    } else if (p.left_mode === 'outline') {
        const tp = textPos(0, lw, leftFontSize, p.left_text_align);
        const s = outlinePath(0, ly, lrw, lh, leftCorners, sw);
        shapes += `
    ${s} fill="${esc(p.color)}"/>`;
        if (p.left_text) {
            shapes += `
    <text fill="${esc(p.color)}" text-anchor="${tp.anchor}" dominant-baseline="central"
          x="${tp.x}" y="${lcy}"
          font-size="${leftFontSize}" font-family="${esc(p.font_family)}, sans-serif"
          font-weight="${fw}">${esc(p.left_text)}</text>`;
        }
    }

    // ---- RIGHT SQUARE ----
    if (p.right_mode === 'outline_filled_letter') {
        const tp = textPos(rx, rw, rightFontSize, p.right_text_align);
        const s = outlinePath(rx, ry, rw, rh, rightCorners, sw);
        shapes += `
    ${s} fill="${esc(p.color)}"/>`;
        if (p.right_text) {
            shapes += `
    <text fill="${esc(p.color)}" text-anchor="${tp.anchor}" dominant-baseline="central"
          x="${tp.x}" y="${rcy}"
          font-size="${rightFontSize}" font-family="${esc(p.font_family)}, sans-serif"
          font-weight="${fw}">${esc(p.right_text)}</text>`;
        }

    } else if (p.right_mode === 'filled_cutout') {
        const tp = textPos(rx, rw, rightFontSize, p.right_text_align);
        const maskShape = squarePath(rx, ry, rw, rh, rightCorners);
        defs += `
    <mask id="mask-right">
      ${maskShape} fill="white"/>
      ${p.right_text ? `<text fill="black" text-anchor="${tp.anchor}" dominant-baseline="central"
            x="${tp.x}" y="${rcy}"
            font-size="${rightFontSize}" font-family="${esc(p.font_family)}, sans-serif"
            font-weight="${fw}">${esc(p.right_text)}</text>` : ''}
    </mask>`;
        const s = squarePath(rx, ry, rw, rh, rightCorners);
        shapes += `
    ${s} fill="${esc(p.color)}" mask="url(#mask-right)"/>`;

    } else if (p.right_mode === 'filled') {
        const tp = textPos(rx, rw, rightFontSize, p.right_text_align);
        const s = squarePath(rx, ry, rw, rh, rightCorners);
        shapes += `
    ${s} fill="${esc(p.color)}"/>`;
        if (p.right_text) {
            shapes += `
    <text fill="${esc(p.color_bg === 'transparent' ? '#ffffff' : p.color_bg)}" text-anchor="${tp.anchor}" dominant-baseline="central"
          x="${tp.x}" y="${rcy}"
          font-size="${rightFontSize}" font-family="${esc(p.font_family)}, sans-serif"
          font-weight="${fw}">${esc(p.right_text)}</text>`;
        }
    }

    const transpOutside = p.transparent_outside === true || p.transparent_outside === 'true';
    const hasBg = p.color_bg && p.color_bg !== 'transparent';
    let bgRect = '';
    if (hasBg) {
        if (transpOutside) {
            // Draw background only inside the box shapes, keeping corners transparent
            const bgL = squarePath(0, ly, lrw, lh, leftCorners);
            const bgR = squarePath(rx, ry, rw, rh, rightCorners);
            bgRect = `\n    ${bgL} fill="${esc(p.color_bg)}"/>\n    ${bgR} fill="${esc(p.color_bg)}"/>`;
        } else {
            bgRect = `\n    <rect width="${totalWidth}" height="${totalHeight}" fill="${esc(p.color_bg)}"/>`;
        }
    }

    // Embed font @font-face if font_embed is provided and there is text
    let fontStyle = '';
    if (p.font_embed && (p.left_text || p.right_text)) {
        fontStyle = `
    <style>
      @font-face {
        font-family: '${esc(p.font_family)}';
        font-weight: ${fw};
        font-style: normal;
        src: url('data:font/woff2;base64,${p.font_embed}') format('woff2');
      }
    </style>`;
    }

    const defsBlock = (defs || fontStyle) ? `\n  <defs>${fontStyle}${defs}\n  </defs>` : '';

    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${totalWidth} ${totalHeight}">\n  <title>${esc(p.filename)}</title>\n  <desc>Generated by logo-generator v${VERSION}</desc>${defsBlock}\n  <g>${bgRect}${shapes}\n  </g>\n</svg>`;
}

/** XML-escape a string value for safe use in SVG attributes and text */
function esc(val) {
    return String(val)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// Export for Node.js (CLI); also available as a global in the browser
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { generateLogoSVG, VERSION };
}
