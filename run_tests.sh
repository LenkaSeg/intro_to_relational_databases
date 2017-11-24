#!/bin/bash
psql < tournament.sql
python tournament_test.py
