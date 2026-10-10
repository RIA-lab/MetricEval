-- Pandoc Lua filter for the LaTeX build (build_latex.py).
-- Turns the structural divs of the Markdown sources into LaTeX environments:
--   image + caption div       -> figure
--   .box / block quote        -> shaded box
--   .tmeta                    -> small shaded box
--   .caption (alone)          -> small text
--   .defs, .excerpt, .toc     -> small / footnote-size text around their tables
-- Other divs (for example .keep-next) are unwrapped.

local function raw(s) return pandoc.RawBlock('latex', s) end

local function wrap(blocks, before, after)
  local out = pandoc.List({ raw(before) })
  out:extend(blocks)
  out:insert(raw(after))
  return out
end

local function is_lone_image(b)
  return b.t == 'Para' and #b.content == 1 and b.content[1].t == 'Image'
end

local function div_to_blocks(el)
  local c = el.classes
  if c:includes('box') then
    return wrap(el.content, '\\begin{shaded}', '\\end{shaded}')
  elseif c:includes('tmeta') then
    return wrap(el.content, '\\begin{shaded}\\small', '\\end{shaded}')
  elseif c:includes('caption') then
    return wrap(el.content, '{\\small', '}')
  elseif c:includes('excerpt') or c:includes('toc') then
    return wrap(el.content, '{\\footnotesize', '}')
  elseif c:includes('defs') then
    return wrap(el.content, '{\\small', '}')
  end
  return el.content
end

function BlockQuote(el)
  return wrap(el.content, '\\begin{shaded}', '\\end{shaded}')
end

function Blocks(blocks)
  local out = pandoc.List()
  local i = 1
  while i <= #blocks do
    local b = blocks[i]
    local nxt = blocks[i + 1]
    if is_lone_image(b) and nxt and nxt.t == 'Div' and nxt.classes:includes('caption') then
      local img = b.content[1]
      out:insert(raw('\\begin{figure}[t]\n\\centering\n\\includegraphics[width=\\linewidth]{' .. img.src .. '}\n\\par\\smallskip'))
      out:extend(wrap(nxt.content, '{\\small', '}'))
      out:insert(raw('\\end{figure}'))
      i = i + 2
    elseif b.t == 'Div' then
      out:extend(div_to_blocks(b))
      i = i + 1
    else
      out:insert(b)
      i = i + 1
    end
  end
  return out
end
