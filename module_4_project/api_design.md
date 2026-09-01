# Module 4 Project — Part 2: Study Tracker API Design

**Your Name:** Timothy
**Date:** September 1, 2026

---

## The App: Study Tracker

Study Tracker helps students record focused study sessions, organize those
sessions by course, and set weekly study goals. It calculates progress from
logged minutes so each student can compare actual study time with the target
for every course.

The examples below use the base path `/api/v1`. JSON is used for all request and
response bodies, datetimes use ISO 8601 UTC format, and resource IDs are UUID
strings.

---

## Section 1 — Resources

| Resource | Key attributes |
|---|---|
| Students | `id`, `email`, `display_name`, `timezone`, `is_active`, `created_at` |
| Courses | `id`, `student_id`, `code`, `name`, `color`, `is_archived`, `created_at` |
| Study Sessions | `id`, `student_id`, `course_id`, `started_at`, `duration_minutes`, `notes`, `completed`, `created_at`, `updated_at` |
| Goals | `id`, `student_id`, `course_id`, `week_start`, `target_minutes`, `active`, `created_at`, `updated_at` |

Progress is a calculated representation rather than a stored resource. It is
derived from a student's goals and completed study sessions for a requested
week.

---

## Section 2 — Relationships

- **Student → Course (one-to-many):** One student can create many courses, and
  each course belongs to exactly one student through `course.student_id`.
- **Student → Study Session (one-to-many):** One student can log many study
  sessions. Each session belongs to the authenticated student through
  `study_session.student_id`.
- **Course → Study Session (one-to-many):** One course can contain many study
  sessions, while each session records work for exactly one course through
  `study_session.course_id`.
- **Student → Goal (one-to-many):** One student can set many weekly goals, while
  each goal belongs to one student through `goal.student_id`.
- **Course → Goal (one-to-many):** A course can have one goal for each week and
  therefore many goals over time. A unique constraint on `(course_id,
  week_start)` prevents duplicate weekly goals.

Ownership is transitive: a student may create a session or goal only for a
course that the same student owns.

---

## Section 3 — Endpoints

### Students

| Method | URI | Description | Auth required? |
|---|---|---|---|
| GET | `/api/v1/students` | List students; intended for administrators. | Yes — admin |
| POST | `/api/v1/students` | Register a new student account. | No |
| GET | `/api/v1/students/{student_id}` | Retrieve one student's profile. | Yes — self or admin |
| PUT | `/api/v1/students/{student_id}` | Replace the editable fields of a student profile. | Yes — self or admin |
| DELETE | `/api/v1/students/{student_id}` | Delete a student and schedule owned data for removal. | Yes — self or admin |

### Courses

| Method | URI | Description | Auth required? |
|---|---|---|---|
| GET | `/api/v1/courses` | List the authenticated student's courses. | Yes |
| POST | `/api/v1/courses` | Create a course for the authenticated student. | Yes |
| GET | `/api/v1/courses/{course_id}` | Retrieve one owned course. | Yes — owner |
| PUT | `/api/v1/courses/{course_id}` | Replace an owned course's editable fields. | Yes — owner |
| DELETE | `/api/v1/courses/{course_id}` | Delete an owned course if retention rules allow it. | Yes — owner |

### Study Sessions

| Method | URI | Description | Auth required? |
|---|---|---|---|
| GET | `/api/v1/study_sessions` | List owned sessions; filter with `course_id`, `start_date`, `end_date`, and/or `completed`. | Yes |
| POST | `/api/v1/study_sessions` | Log a study session for an owned course. | Yes |
| GET | `/api/v1/study_sessions/{session_id}` | Retrieve one owned study session. | Yes — owner |
| PUT | `/api/v1/study_sessions/{session_id}` | Replace an owned study session's editable fields. | Yes — owner |
| DELETE | `/api/v1/study_sessions/{session_id}` | Delete an owned study session. | Yes — creator/owner |

Filtering example:

```http
GET /api/v1/study_sessions?course_id=71f7d929-a59f-4f06-994f-c2ad8ca0f72d&start_date=2026-08-31&end_date=2026-09-06&completed=true
```

All filters are optional and combined with logical **AND**. `start_date` and
`end_date` are interpreted in the student's configured timezone. Collection
responses are paginated with optional `limit` and `cursor` parameters.

### Goals

| Method | URI | Description | Auth required? |
|---|---|---|---|
| GET | `/api/v1/goals` | List owned goals; optionally filter by `course_id`, `week_start`, or `active`. | Yes |
| POST | `/api/v1/goals` | Set a weekly goal for an owned course. | Yes |
| GET | `/api/v1/goals/{goal_id}` | Retrieve one owned weekly goal. | Yes — owner |
| PUT | `/api/v1/goals/{goal_id}` | Replace an owned weekly goal's editable fields. | Yes — owner |
| DELETE | `/api/v1/goals/{goal_id}` | Delete an owned weekly goal. | Yes — creator/owner |

### Progress and Authentication

| Method | URI | Description | Auth required? |
|---|---|---|---|
| GET | `/api/v1/students/{student_id}/progress?week_start={date}` | Return calculated totals and goal progress for one week. | Yes — self or admin |
| POST | `/api/v1/auth/token` | Exchange valid email/password credentials for a JWT access token. | No |

There are **22 endpoints total**, including full CRUD for all four stored
resources and filtering endpoints for both sessions and goals.

---

## Section 4 — Request/Response Schemas

### POST `/api/v1/study_sessions` — Create a new session

The server gets `student_id` from the JWT rather than trusting a client-supplied
owner ID. An optional `Idempotency-Key` request header prevents accidental
duplicate creation when a client retries the same request.

**Request body fields:**

| Field | Type | Required? | Validation/meaning |
|---|---|---|---|
| `course_id` | string (UUID) | Yes | Must identify a course owned by the authenticated student. |
| `started_at` | string (datetime) | Yes | ISO 8601 datetime with a UTC offset; cannot be unreasonably far in the future. |
| `duration_minutes` | integer | Yes | Whole number from 1 through 1,440. |
| `notes` | string or null | No | Plain text, maximum 2,000 characters; defaults to `null`. |
| `completed` | boolean | No | Whether the session counts toward progress; defaults to `true`. |

```json
{
  "course_id": "71f7d929-a59f-4f06-994f-c2ad8ca0f72d",
  "started_at": "2026-09-01T18:30:00Z",
  "duration_minutes": 90,
  "notes": "Reviewed chapters 4 and 5",
  "completed": true
}
```

**Success response — `201 Created`:**

```json
{
  "id": "ba04ed31-49b0-4e62-b1f8-f6997205bef6",
  "student_id": "ad791d46-47fe-4be0-9240-09caa516cbef",
  "course_id": "71f7d929-a59f-4f06-994f-c2ad8ca0f72d",
  "started_at": "2026-09-01T18:30:00Z",
  "duration_minutes": 90,
  "notes": "Reviewed chapters 4 and 5",
  "completed": true,
  "created_at": "2026-09-01T20:05:14Z",
  "updated_at": "2026-09-01T20:05:14Z"
}
```

The response fields have the same types as the request fields. `id`,
`student_id`, and `course_id` are UUID strings; `created_at` and `updated_at`
are datetime strings. The response also includes a `Location` header containing
`/api/v1/study_sessions/{new_session_id}`.

### POST `/api/v1/goals` — Create a weekly goal

**Request body fields:**

| Field | Type | Required? | Validation/meaning |
|---|---|---|---|
| `course_id` | string (UUID) | Yes | Must identify a course owned by the authenticated student. |
| `week_start` | string (date) | Yes | Calendar date in `YYYY-MM-DD` format; must be a Monday. |
| `target_minutes` | integer | Yes | Weekly target from 1 through 10,080 minutes. |
| `active` | boolean | No | Whether progress should display this goal; defaults to `true`. |

```json
{
  "course_id": "71f7d929-a59f-4f06-994f-c2ad8ca0f72d",
  "week_start": "2026-08-31",
  "target_minutes": 300,
  "active": true
}
```

**Success response — `201 Created`:**

```json
{
  "id": "8a69d057-f695-4798-af3f-f3121b7519c8",
  "student_id": "ad791d46-47fe-4be0-9240-09caa516cbef",
  "course_id": "71f7d929-a59f-4f06-994f-c2ad8ca0f72d",
  "week_start": "2026-08-31",
  "target_minutes": 300,
  "active": true,
  "created_at": "2026-09-01T20:10:00Z",
  "updated_at": "2026-09-01T20:10:00Z"
}
```

Here, IDs are UUID strings, `week_start` is a date string, `target_minutes` is
an integer, `active` is a boolean, and both timestamps are datetime strings.

### GET `/api/v1/study_sessions/{session_id}` — Retrieve a session

**Response fields:**

| Field | Type | Meaning |
|---|---|---|
| `id` | string (UUID) | Unique session identifier. |
| `student_id` | string (UUID) | Owner of the session. |
| `course_id` | string (UUID) | Course studied during the session. |
| `started_at` | string (datetime) | ISO 8601 start time. |
| `duration_minutes` | integer | Logged duration in whole minutes. |
| `notes` | string or null | Optional session notes. |
| `completed` | boolean | Whether the session contributes to progress. |
| `created_at` | string (datetime) | Creation timestamp. |
| `updated_at` | string (datetime) | Most recent update timestamp. |

**Response — `200 OK`:**

```json
{
  "id": "ba04ed31-49b0-4e62-b1f8-f6997205bef6",
  "student_id": "ad791d46-47fe-4be0-9240-09caa516cbef",
  "course_id": "71f7d929-a59f-4f06-994f-c2ad8ca0f72d",
  "started_at": "2026-09-01T18:30:00Z",
  "duration_minutes": 90,
  "notes": "Reviewed chapters 4 and 5",
  "completed": true,
  "created_at": "2026-09-01T20:05:14Z",
  "updated_at": "2026-09-01T20:05:14Z"
}
```

### GET `/api/v1/students/{student_id}/progress` — Retrieve weekly progress

This endpoint accepts a required `week_start` query parameter with a
`YYYY-MM-DD` Monday date.

**Response fields:**

| Field | Type | Meaning |
|---|---|---|
| `student_id` | string (UUID) | Student whose progress was calculated. |
| `week_start` | string (date) | First date included in the calculation. |
| `week_end` | string (date) | Last date included in the calculation. |
| `total_studied_minutes` | integer | Sum of all completed sessions in the week. |
| `total_target_minutes` | integer | Sum of all active goals in the week. |
| `overall_percent_complete` | number (decimal) | Overall progress percentage; may exceed 100. |
| `goals` | array of objects | Per-course progress entries described below. |
| `generated_at` | string (datetime) | Time at which the summary was calculated. |

Each object in `goals` contains `goal_id` (UUID string), `course_id` (UUID
string), `course_name` (string), `target_minutes` (integer),
`studied_minutes` (integer), `remaining_minutes` (integer), `percent_complete`
(decimal number), and `met` (boolean).

**Response — `200 OK`:**

```json
{
  "student_id": "ad791d46-47fe-4be0-9240-09caa516cbef",
  "week_start": "2026-08-31",
  "week_end": "2026-09-06",
  "total_studied_minutes": 270,
  "total_target_minutes": 300,
  "overall_percent_complete": 90.0,
  "goals": [
    {
      "goal_id": "8a69d057-f695-4798-af3f-f3121b7519c8",
      "course_id": "71f7d929-a59f-4f06-994f-c2ad8ca0f72d",
      "course_name": "Biology 101",
      "target_minutes": 300,
      "studied_minutes": 270,
      "remaining_minutes": 30,
      "percent_complete": 90.0,
      "met": false
    }
  ],
  "generated_at": "2026-09-06T23:59:00Z"
}
```

---

## Section 5 — Authentication

### Method and rationale

The API uses **JWT bearer authentication**. A student signs in through
`POST /api/v1/auth/token`; after the credentials are verified, the server
returns a short-lived access token. Clients send it with protected requests:

```http
Authorization: Bearer <access_token>
```

JWT is appropriate because the API can verify identity and roles without
requiring an API key to be embedded permanently in a student application.
Tokens should expire after 15 minutes; a secure refresh-token flow can issue a
new access token. Passwords are salted and hashed and are never placed in a
token or response.

### Public and protected access

| Endpoint or group | Auth required? | Access rule |
|---|---|---|
| `POST /students` | No | Public registration with validation and rate limiting. |
| `POST /auth/token` | No | Public sign-in with credential checking and rate limiting. |
| `GET /students` | Yes | Administrator role only. |
| `GET`, `PUT`, `DELETE /students/{student_id}` | Yes | Matching student or administrator only. |
| Course endpoints | Yes | Students can access only courses they own. |
| Study-session endpoints | Yes | Students can access only sessions they created; only the creator can update or delete. |
| Goal endpoints | Yes | Students can access only goals attached to their own courses; only the creator can update or delete. |
| `GET /students/{student_id}/progress` | Yes | Matching student or administrator only. |

The server reads the student ID and role from verified JWT claims. It never
accepts a request-body `student_id` as proof of ownership. When an authenticated
student requests another student's private resource, the API returns `404` to
avoid revealing whether that resource exists. Administrators may access student
profiles and progress for support purposes, but they do not silently edit study
sessions or goals.

---

## Section 6 — Error Responses for POST `/api/v1/study_sessions`

| Status code | When it occurs |
|---|---|
| `201 Created` | The session is valid and was created. The body contains the new resource and the `Location` header contains its URI. |
| `400 Bad Request` | The JSON is malformed, the request body is missing, or a field has the wrong basic JSON type. |
| `401 Unauthorized` | The bearer token is missing, expired, malformed, or has an invalid signature. |
| `403 Forbidden` | The token is valid, but the account is inactive or a role policy prohibits session creation. |
| `404 Not Found` | `course_id` does not exist or belongs to another student. The same response prevents ownership information from leaking. |
| `409 Conflict` | The same `Idempotency-Key` was previously used with a different request body. |
| `413 Content Too Large` | The request body exceeds the server's configured size limit. |
| `415 Unsupported Media Type` | The request does not use `Content-Type: application/json`. |
| `422 Unprocessable Content` | JSON is valid, but a value violates a rule—for example, duration is outside 1–1,440, notes exceed 2,000 characters, or the datetime is invalid. |
| `429 Too Many Requests` | The student or client has exceeded the endpoint's rate limit. A `Retry-After` header indicates when to retry. |
| `500 Internal Server Error` | An unexpected server failure occurs. The response includes a request ID but no sensitive implementation details. |
| `503 Service Unavailable` | A required service, such as the database, is temporarily unavailable. A retry may succeed later. |

All error responses use one consistent JSON shape:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request contains invalid fields.",
    "details": [
      {
        "field": "duration_minutes",
        "issue": "must be between 1 and 1440"
      }
    ],
    "request_id": "req_01K45N3Y7V8RG2X9K9T9SMT1F4"
  }
}
```

`details` is an array and may be empty for errors that are not field-specific.
The stable machine-readable `code` helps clients react without parsing the
human-readable `message`.
