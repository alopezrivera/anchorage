import waybackpy

from Alexandria.general.console import print_color


def archive(name, url, user_agent=None):
    try:
        wind = waybackpy.Url(url, user_agent) if not isinstance(user_agent, type(None)) else waybackpy.Url(url)
        stone = wind.save()
        return stone.archive_url
    except waybackpy.exceptions.WaybackError as e:
        print(f"{e}")
        print(f"        {name}")
        print(f"        {url}")


print(archive('Functors and Monads For People Who Have Read Too Many "Tutorials" - iRi',
              "http://www.jerf.org/iri/post/2958",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:40.0) Gecko/20100101 Firefox/40.0"))



