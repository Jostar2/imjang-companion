# Project Brief

## Project Name

Imjang Companion MVP

## Problem Statement

Property buyers and small-scale investors visit multiple apartments or houses in a short period and lose track of notes, photos, red flags, and comparison criteria. Most field visit notes are scattered across messaging apps, gallery photos, and spreadsheets, which makes later decision-making unreliable.

## Users

- primary user: individual property buyer
- secondary user: small-scale real estate investor
- optional internal user: research assistant or partner reviewing the same visit notes

## Goal

Build a mobile-first web product that lets users prepare a visit checklist, capture structured notes during a field visit, score the property and neighborhood, compare candidates, and generate a summary report after the visit.

## Scope

### Included

- create a visit project
- add candidate properties manually
- store listing metadata
- run a standardized visit checklist
- capture notes, ratings, and photos
- compare visited properties
- generate a shareable summary report

### Excluded

- live brokerage integration
- mortgage or loan workflow
- legal due diligence automation
- production OCR of registry or contract documents
- multi-user realtime collaboration

## Preferred Stack

- frontend: Next.js
- backend: FastAPI
- database: PostgreSQL
- file storage: S3-compatible object storage
- infra: AWS ECS

## Constraints

- mobile-first UX is required
- staging readiness is required
- production deploy remains human-approved
- first version should not require complex external listing integrations
- offline full-sync is out of scope, but draft-save behavior should be considered

## Success Criteria

- a user can create a visit project and register candidate properties
- a user can complete a visit checklist with notes, scores, and photos
- a user can compare at least two properties with a summary view
- staging smoke test verifies create project, add property, complete visit, and view report

## Acceptance Hints

- required checklist sections must be completed before a visit is marked complete
- photo uploads must be attached to the correct property visit
- comparison view must show total score plus key red flags
- summary report must include visit date, top findings, and recommendation notes

## Release Notes

This first run should stop at planning, architecture, bounded task packets, and staging readiness artifacts.
