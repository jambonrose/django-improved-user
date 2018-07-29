####################################
Warning about Email Case-Sensitivity
####################################

`RFC 5321`_ states that the ``mailbox`` in ``mailbox@hostname`` of an
email format is case-sensitive. ``ANDREW@example.com`` and
``andrew@example.com`` are therefore different email addresses (the
domain is case-insensitive).

Django's :class:`~django.db.models.EmailField` follows the RFC, and so,
therefore, does Improved User.

Today, many email providers have made their email systems
case-insensitive. However, not all providers have done so. As such, if
we were to provide a custom case-insensitive ``EmailField``, we may be
alienating your users without you even knowing!

What's more, we follow the RFC because not doing so can `cause obscure
security issues`_.

When creating your project's templates, we recommend reminding your
users that their emails *may* be case-sensitive, and that the username
on this site is definitely case-sensitive.

Even if email case-sensitivity becomes a problem on your site, we
recommend you continue to use case-sensitive email fields so that you
retain case-sensitive data. Instead, rely on case-insensitive selection
and filtering to find and authenticate users (lowercase database indexes
can make this quite fast). These decisions and code are outside the
scope of this project and we therefore do not provide any work on this
front.

.. _`RFC 5321`: https://tools.ietf.org/rfc/rfc5321.txt
.. _`cause obscure security issues`: https://www.schneier.com/blog/archives/2018/04/obscure_e-mail_.html

