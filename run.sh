#!/bin/env bash

sudo docker-compose down

sudo docker-compose build

sudo docker-compose up -d

sleep 5

sudo docker-compose ps
