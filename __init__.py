from aqt.deckbrowser import DeckBrowser
import html

#this is a copy of the _render_deck_node function
def render_deck_node(self, node, ctx) -> str:
		if node.collapsed:
			prefix = "+"
		else:
			prefix = "-"

		def indent() -> str:
			return "&nbsp;" * 6 * (node.level - 1)

		if node.deck_id == ctx.current_deck_id:
			klass = "deck current"
		else:
			klass = "deck"

		buf = (
			"<tr class='%s' id='%d' onclick='if(event.shiftKey) return pycmd(\"select:%d\")'>"
			% (
				klass,
				node.deck_id,
				node.deck_id,
			)
		)
		# deck link
		if node.children:
			collapse = (
				"<a class=collapse href=# onclick='return pycmd(\"collapse:%d\")'>%s</a>"
				% (node.deck_id, prefix)
			)
		else:
			collapse = "<span class=collapse></span>"
		if node.filtered:
			extraclass = "filtered"
		else:
			extraclass = ""
		buf += """

		<td class=decktd colspan=5>%s%s<a class="deck %s"
		href=# onclick="return pycmd('open:%d')">%s</a></td>""" % (
			indent(),
			collapse,
			extraclass,
			node.deck_id,
			html.escape(node.name),
		)

		# due counts
		def nonzeroColour(cnt: int, klass: str) -> str:
			if not cnt:
				klass = "zero-count"
			return f'<span class="{klass}">{cnt}</span>'
		
		review = nonzeroColour(node.review_count, "review-count")
		learn = nonzeroColour(node.learn_count, "learn-count")
		dnew = nonzeroColour(node.new_count, "new-count")

		#this is the only change made to the function
		if not node.collapsed:
			review = nonzeroColour(node.review_count, "zero-count")
			learn = nonzeroColour(node.learn_count, "zero-count")
			dnew = nonzeroColour(node.new_count, "zero-count")

		buf += ("<td align=end>%s</td>" * 3) % (
			dnew,
			learn,
			review,
		)
		# options
		buf += (
			"<td align=center class=opts><a onclick='return pycmd(\"opts:%d\");'>"
			"<img src='/_anki/imgs/gears.svg' class=gears></a></td></tr>" % node.deck_id
		)
		# children
		if not node.collapsed:
			for child in node.children:
				buf += self._render_deck_node(child, ctx)
		return buf



DeckBrowser._render_deck_node = render_deck_node