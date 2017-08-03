#!/usr/bin/env python
from app import create_app
from app import celery
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
if __name__ == '__main__':
    app.run()
