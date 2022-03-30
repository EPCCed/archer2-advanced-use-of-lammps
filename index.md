---
layout: lesson
carpentry: "swc"
venue: 
address: 
country: "UK"
language: "English"
latlng: 
humandate: 
humantime: 
startdate: 
enddate: 
instructor: ["Julien Sindt and Stephen Farr"]
helper: ["Andy Turner"]
email: ["J.Sindt@epcc.ed.ac.uk"]
collaborative_notes: 
eventbrite: 
root: .
---

<h2>Description</h2>

This lesson provides an overview of some more advanced techniques and uses of 
LAMMPS. Specifically, we will be discussing:
  - Measuring and improving LAMMPS performance
  - Using LAMMPS with Python
  - Analysing systems through reruns
  - Advanced sampling methods with a focus on replica exchange

For this lesson, we expect attendees to be familiar with LAMMPS. We will *not* 
be covering how to prepare and run a parallel LAMMPS simulation (and we will 
assume that all attendees know how to do that already). This lesson is aimed 
at anyone who:
  - has experience using `bash` (or any other shell)
  - has experience running LAMMPS on multiple processors

<hr/>

<h2 id="general">General Information</h2>

{% comment %}
  LOCATION

  This block displays the address and links to maps showing directions
  if the latitude and longitude of the workshop have been set.  You
  can use https://itouchmap.com/latlong.html to find the lat/long of an
  address.
{% endcomment %}
{% if page.latlng %}
<p id="where">
  <strong>Where:</strong>
  {{page.address}}.
  Get directions with
  <a href="//www.openstreetmap.org/?mlat={{page.latlng | replace:',','&mlon='}}&zoom=16">OpenStreetMap</a>
  or
  <a href="//maps.google.com/maps?q={{page.latlng}}">Google Maps</a>.
</p>
{% endif %}

{% comment %}
  DATE

  This block displays the date and links to Google Calendar.
{% endcomment %}
{% if page.humandate %}
<p id="when">
  <strong>When:</strong>
  {{page.humandate}}.
  {% include workshop_calendar.html %}
</p>
{% endif %}

{% comment %}
  SPECIAL REQUIREMENTS

  Modify the block below if there are any special requirements.
{% endcomment %}
<p id="requirements">
  <strong>Requirements:</strong> Participants must have a working laptop or 
  desktop computer with a Mac, Linux, or Windows operating system (not a 
  tablet, Chromebook, etc.) that they have administrative privileges on. They 
  should have access to a terminal (Max and Linux users should have a terminal 
  installed by default; Windows users should get either 
  <a href="https://mobaxterm.mobatek.net/">MobaXterm</a> or 
  <a href="https://www.putty.org/">PuTTY</a>. They are also required to abide 
  by the <a href="https://www.archer2.ac.uk/training/code-of-conduct/">ARCHER2 Training Code of Conduct</a>.
</p>

{% comment %}
  ACCESSIBILITY

  Modify the block below if there are any barriers to accessibility or
  special instructions.
{% endcomment %}
<p id="accessibility">
  <strong>Accessibility:</strong> We are committed to making this workshop
  accessible to everybody.
  The workshop organizers have checked that:
</p>
<ul>
  <li>The room is wheelchair / scooter accessible.</li>
  <li>Accessible restrooms are available.</li>
</ul>
<p>
  Materials will be provided in advance of the lesson and
  large-print handouts are available if needed by notifying the
  organizers in advance.  If we can help making learning easier for
  you (e.g. sign-language interpreters, lactation facilities) please
  get in touch (using contact details below) and we will
  attempt to provide them.
</p>

{% comment %}
  CONTACT EMAIL ADDRESS

  Display the contact email address set in the configuration file.
{% endcomment %}
<p id="contact">
  <strong>Contact</strong>:
  Please email
  {% if page.email %}
    {% for email in page.email %}
      {% if forloop.last and page.email.size > 1 %}
        or
      {% else %}
        {% unless forloop.first %}
        ,
        {% endunless %}
      {% endif %}
      <a href='mailto:{{email}}'>{{email}}</a>
    {% endfor %}
  {% else %}
    to-be-announced
  {% endif %}
  for more information.
</p>

<hr/>

> ## Prerequisites
> You should have used remote HPC facilities before. In particular, you should be happy with connecting
> using SSH, know what a batch scheduling system is and be familiar with using the Linux command line.
> You should also be happy editing plain text files in a remote terminal (or, alternatively, editing them
> on your local system and copying them to the remote HPC system using `scp`).
{: .prereq}

<hr/>

{% include links.md %}

