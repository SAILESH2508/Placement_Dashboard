import json
from django.db import models
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.models import Student
from companies.models import Company
from placements.models import Job, Application
from notifications.models import Notification

# Legacy dashboard view removed. Use API.
