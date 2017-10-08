#################
Project Rationale
#################

While working together in late 2016, `Russell Keith-Magee`_ and `Andrew
Pinkham`_— original authors of the project—discussed the repetitive
nature of rebuilding a best-practices email-based User model in new
Django projects. The two were tired of redoing the same work, and
decided to open-source code based on what they'd learned previously.

Russell's *Red User, Blue User, MyUser, auth.User* talk from DjangoCon
US 2013 and PyCon AU 2017 (video below) provides a breakdown of the
problems with Django's existing approach to identity-handling, as well
as an introduction to using custom User models in Django.

.. raw:: html

    <center>
    <iframe width="560" height="315" src="https://www.youtube.com/embed/458KmAKq0bQ?list=PLs4CJRBY5F1KsK4AbFaPsUT8X8iXc7X84" frameborder="0" allowfullscreen></iframe>
    </center>

In turn, Andrew was frustrated by the lack of modularity in Django's
existing ``auth`` codebase. Having described (in painstaking detail) the
process of creating custom User models in `his book, Django Unleashed`_,
Andrew felt that developers should be able to import and compose classes
to properly integrate with Django's permissions and/or admin. The two
set out to build a project that would:

1. provide a User model that authenticates via email (not username)
2. provide a User model with global identity name-fields (full name and short
   name, rather than the limited anglo-centric first and last name)
3. provide mix-in classes to allow developers to easily compose a new
   User model.

The project is originally based on the app that Russell had built over a
decade of working in Django. Andrew took what he had learned from
`Django Unleashed`_ and his `consulting experience`_, and integrated it
into the project. The result is a :class:`~improved_user.models.User`
model that can be used out of the box (see :doc:`quickstart` for
details) and a set of :doc:`mix-in classes <source/mixin_models>` to
allow for creation of new User models (notably, the
:class:`~improved_user.mixins.DjangoIntegrationMixin`).

We hope you find our work useful!

.. _Andrew Pinkham: http://andrewsforge.com
.. _consulting experience: https://www.jambonsw.com
.. _Django Unleashed: https://django-unleashed.com
.. _his book, Django Unleashed: `Django Unleashed`_
.. _Russell Keith-Magee: https://cecinestpasun.com
