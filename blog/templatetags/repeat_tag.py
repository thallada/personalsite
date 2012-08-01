# Credit to alex-dev for this very useful template tag.
from django.template import Library
from django.template import Node, NodeList
from django.template import TemplateSyntaxError

register = Library()

class RepeatNode(Node):
    def __init__(self, repeatvar, recursionvar, is_tree):
        self.repeatvar, self.recursionvar = repeatvar, recursionvar
        self.is_tree = is_tree or (self.sequencevar is not None)

    def __repr__(self):
        recursion = self.recursionvar
        if self.is_tree:
            recursion = "each %s" % self.recursionvar
        return "<Repeat Node: repeat %s for %s>" % (recursion, self.repeatvar)

    def repeat_render(self, context):
        sub_sequence = self.recursionvar.resolve(context, True)
        if self.is_tree:
            if len(sub_sequence):
                return self.do_render(context, sub_sequence)
        else:
            if sub_sequence:
                return self.do_render(context, [sub_sequence]) # (trick) sequence of one item
        return ''

    def do_render(self, context, sequence):
        nodelist = NodeList()
        context.push()
        for item in sequence:
            context[self.repeatvar.token] = item
            for node in self.nodelist:
                nodelist.append(node.render(context))

        context.pop()
        return nodelist.render(context)

    def render(self, context):
        return self.do_render(context, [self.repeatvar.resolve(context, True)])

class RepeatHereNode(Node):
    # this node is kind of hook, it only 'redirects' render to master (enclosing 'repeat' tag)
    def __init__(self, master_node):
        self.master_node = master_node

    def render(self, context):
        if self.master_node:
            return self.master_node.repeat_render(context)
        return ''

@register.tag
def repeat(parser, token):
    """
    Tree recursion:
        {% repeat each message.replies for message %}
            <div>{{ message.subject }}
        {% repeat_here %}
            </div>
        {% endrepeat %}

    Chain recursion:
        {% repeat message.reply_to for message %}
            <div>{{ message.subject }}
        {% repeat_here %}
            </div>
        {% endrepeat %}
    
    Note: {% repeat_here %} is optional, if not provided, there would be no recursion.
    """

    def check(condition):
        if not condition:
            raise TemplateSyntaxError("'repeat' statement syntax error: %s" % token.contents)

    bits = token.split_contents()
    check(4 <= len(bits) <= 5)
    # 4 <= len <= 5: repeat[ each] y for x
    check(bits[-2] == 'for')
    repeatvar = parser.compile_filter(bits.pop())
    bits.pop() # == 'for'
    recursionvar = parser.compile_filter(bits.pop())

    # 1 <= len <= 2: repeat[ each]
    is_tree = False
    if len(bits) == 2:
        check(bits[1] == 'each')
        is_tree = True

    node = RepeatNode(repeatvar, recursionvar, is_tree)
    if not hasattr(parser, '_repeatNodesStack'): # this is hack for 'communicating' with repeat_here tag
        parser._repeatNodesStack = []
    parser._repeatNodesStack.append(node)
    node.nodelist = parser.parse(('endrepeat',))
    parser.delete_first_token()
    parser._repeatNodesStack.pop()

    return node

@register.tag
def repeat_here(parser, token):
    bits = token.split_contents()
    if len(bits) != 1:
        raise TemplateSyntaxError("'repeat_here' doesn't take any arguments: %s" % token.contents)
    if not hasattr(parser, '_repeatNodesStack') or len(parser._repeatNodesStack) == 0:
        raise TemplateSyntaxError("'repeat_here' tag used outside 'repeat' tag")
    return RepeatHereNode(parser._repeatNodesStack[-1])

