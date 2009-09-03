import logging, os, zc.buildout


WSGI_INIT = """
WSGIDaemonProcess %s user=%s group=%s threads=%s
WSGIProcessGroup %s
WSGIScriptAlias %s %s
"""

DEFLATED_PATH = """
	<Location %s>
		######### Mod Deflate ########
		SetOutputFilter DEFLATE

		# Netscape 4.x has some problems...
		BrowserMatch ^Mozilla/4 gzip-only-text/html

		# Netscape 4.06-4.08 have some more problems
		BrowserMatch ^Mozilla/4\.0[678] no-gzip

		# MSIE masquerades as Netscape, but it is fine
		BrowserMatch \bMSIE !no-gzip !gzip-only-text/html

		# NOTE: Due to a bug in mod_setenvif up to Apache 2.0.48
		# the above regex won't work. You can use the following
		# workaround to get the desired effect:
		#BrowserMatch \bMSI[E] !no-gzip !gzip-only-text/html

		# Don't compress images
		SetEnvIfNoCase Request_URI \.(?:gif|jpe?g|png)$ no-gzip dont-vary

		# Make sure proxies don't deliver the wrong content
		Header append Vary User-Agent env=!dont-vary

	</Location>
"""
	
STATIC_CONTENTS = """Alias "%s" "%s"
"""

class DjangoWsgiConfig(object):
    def __init__(self, buildout, name, options):
        self.name, self.buildout, self.options = name, buildout, options
                
    def install(self):
        daemon_process = self.options['daemon_process']
        process_group = self.options['process_group']
        user = self.options['user']
        group = self.options['group']
        threads = self.options.get('threads','1')
        
        script_url_location = self.options.get('script_url_location','/')
        script = self.options.get('script',os.path.join(self.buildout['buildout']['bin-directory'],'django.wsgi'))
        
        install_location = self.options.get('install_location',os.path.join(self.buildout['buildout']['bin-directory'],'vhost.conf'))
        
        project_dir = self.buildout.get('django','django').get('project','project')
        
        media_url = self.options.get('media-url','/media')
        django_project_path = os.path.join(self.buildout['buildout']['directory'],project_dir)
        
        media_path =  self.options.get('media-path', os.path.join(django_project_path, 'media'))
        
        admin_media_url = self.options.get('admin-media-url','/amedia')
        admin_media_path = self.options.get('admia-media-path',
            os.path.join(self.buildout['buildout']['parts-directory'],'django/django/contrib/admin/media')
        )
                
        config = (WSGI_INIT % (daemon_process, user, group, threads, process_group, script_url_location, script)+
            DEFLATED_PATH % script_url_location +
            STATIC_CONTENTS % (media_url,media_path) +
            STATIC_CONTENTS % (admin_media_url,admin_media_path))

        logging.getLogger(self.name).info('writing apache conf file')
        
        vhost_conf = file(install_location,'w+')
        vhost_conf.write(config)
        vhost_conf.close()
                
        return install_location
        
    def update(self):
        install(self)

