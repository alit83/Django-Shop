{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{ token }}
{% endblock %}

{% block body %}
This is a plain text part.
{% endblock %}

{% block html %}
{{site_domain}}/accounts/verify-email/{{token}}/
{% endblock %}