# -*- coding: utf-8 -*-
"""Simple wrapper around standard lib email support."""
from email.mime.text import MIMEText


def comma_strlist(strlist):
    if isinstance(strlist, basestring):
        return strlist
    elif isinstance(strlist, list):
        return ', '.join(strlist)


class RawMailer(object):
    """Manage and send mails."""

    def __init__(self, config, mail_env):
        self._mail_env = mail_env
        self._config = config

    def send(self, mail_tpl, to, mail_args):
        """Process a mail request.

        Arguments:
            mail_tpl -- (str) name of the mail template
            to -- (str or list) recipient(s) mail address(es)
            mail_args -- (dict) arguments which will be passed to mail
                         template

        Example:
            mailer.send('sub/test', 'aa@bb.cc', {'foo': u'bar'})

        """
        (subject, content) = self._render_mail(mail_tpl, mail_args)

        msg = MIMEText(content.encode('utf-8'), 'plain', 'utf-8')
        msg['From'] = self._config['MAIL_FROM']
        msg['Subject'] = subject
        msg['To'] = comma_strlist(to)

        if self._config.get('MAIL_OVERRIDE_TO'):
            to = self._config['MAIL_OVERRIDE_TO']

        return self._send(to, msg)

    def _render_mail(self, mail_tpl, mail_args):
        """Render and return a mail content.

        Arguments:
            see `send()`

        """
        _mail_args = dict(mail_args.items() + self._config.items())
        template = self._mail_env.get_template(mail_tpl)
        full_mail = template.render(**_mail_args)

        # Subject then body
        return (
            full_mail.splitlines()[0],
            '\n'.join(full_mail.splitlines()[2:]),
        )

    def _send(self, to, msg):
        """Subclasses must implement this method to actually send the
        mail.

        """
        raise NotImplementedError
