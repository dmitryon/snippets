from django import template
register = template.Library()

DEFAULT_TRACKER_ID = "UA-xxxxxxx-x"

class RenderNode(template.Node):
    def __init__(self, tracker_id):
        self.tracker_id = tracker_id

    def render(self, context):
        if not self.tracker_id:
            self.tracker_id = DEFAULT_TRACKER_ID
        content = """
            <script type="text/javascript">

              var _gaq = _gaq || [];
              _gaq.push(['_setAccount', '%s']);
              _gaq.push(['_trackPageview']);

              (function() {
                var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
                ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
                var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
              })();

            </script>
        """ % self.tracker_id
        return content


@register.tag(name='google_analytics')
def render_tag(parser, token):
    parts = token.split_contents()
    tracker_id = None
    if len(parts) > 1:
        tracker_id = parts[-1]
    return RenderNode(tracker_id)

render_tag.is_safe = True
  