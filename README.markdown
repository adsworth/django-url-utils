# django url\_utils #
is a django application with some url helper functionality.

Currently it provides a template tag to generate a project specific url/permalink for a model. This can be used instead of the models `get_absolute_url` method when reusing django apps whose the `get_absolute_url` method don't generate the urls you would like to use in your project.

# Simple Example #

A little Example using the excellent [Coltrane](http://code.google.com/p/coltrane-blog/) blog application. Coltranes get\_absolute\_url generates the following URLs /2009/Feb/10/the\_slug. The month name is abbreviated. I wanted my permalinks to use the months number i.e. /2009/02/10/the\_slug.

My first solution was the included template tag `url`, which looked something like this:

    {% url blog_entry_detail object.pub_date|date:"Y" object.pub_date|date:"m" object.pub_date|date:"d" object.slug %}

I don't think thats very nice. So I came up with the get\_permalink template tag.

Let's get started.

1.  Activate the app by adding url\_utils to your INSTALLED_APPS.
2.  Create an entry in your urls.py to suit your needs.
    
    Mine looks like:
    
        url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        views.object_detail,
        dict(entry_info_dict, month_format='%m', slug_field='slug'),
        name = 'blog_entry_detail'),

3.  Create a permalinks.py file in your projects root dir or somewhere on your python path.
4.  The permalinks module needs to contain a class which has the same name as the application whose model we want to create permalinks for. We then need to create one classmethod for each model we create permalinks for. The method name needs to be get\_&lt;MODELNAME&gt;\_url. The method also needs one parameter the object is will create the permalink for. All names are lower cased.

        from django.core.urlresolvers import reverse

        class coltrane(object):
            @classmethod
            def get_entry_url(cls, entry):
                return reverse( 'blog_entry_detail', 
                        kwargs = { 'year': entry.pub_date.strftime('%Y'),
                                   'month': entry.pub_date.strftime('%m'),
                                   'day': entry.pub_date.strftime('%d'),
                                   'slug': entry.slug })

5.  Now update the templates. Load the template library and use the new tags.

        {% load url_utils_tags %}
        
        {% get_permalink entry%}

6.  That's it
