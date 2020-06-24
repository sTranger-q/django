#!/bin/bash
cd /home/project/comic_mlgm
celery -A comic_mlgm worker -l info
