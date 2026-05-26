# JSON to TypeScript Type Generator

A deterministic TypeScript interface generator built in Python that converts JSON arrays into exact `.d.ts` interface declarations.

The generator supports nested objects, arrays, optional fields, union types, and deterministic naming while strictly following formatting and ordering rules.

---

## Features

- Deterministic TypeScript interface generation
- Nested object handling
- Recursive schema inference
- Array type inference
- Optional field detection
- Union type generation
- Collision-safe interface naming
- Deterministic ordering and formatting
- Support for nullable values

---

## Problem Statement

Given a JSON array of objects, generate TypeScript interface declarations that exactly match a predefined deterministic output format.

The system must:

- Infer types from JSON values
- Merge schemas across multiple objects
- Detect optional fields
- Handle nested objects and arrays
- Resolve interface naming collisions
- Produce deterministic output with strict formatting

---

## Tech Stack

- **Python**
- **JSON Parsing**
- **DFS Traversal**
- **Recursive Schema Processing**
- **Hash Maps / Dictionaries**
- **Type Inference**

---

## Project Structure

```txt
.
├── solution.py
├── README.md
├── sample_input.txt
└── sample_output.txt
```

---

## Example

### Sample Input

```txt
1
CompanyData
[{"id":1,"name":"Alice","email":"alice@example.com","profile":{"age":28,"location":{"city":"New York","zip":"10001"},"skills":["Python","TypeScript"],"experience":5},"projects":[{"title":"Analytics Dashboard","completed":true,"budget":5000},{"title":"ML Pipeline","completed":false}],"metadata":{"verified":true,"score":95.5}},{"id":2,"name":"Bob","profile":{"age":32,"location":{"city":"San Francisco"},"skills":["Java","AWS"]},"projects":[{"title":"Cloud Migration","completed":true}],"metadata":null},{"id":"EMP003","name":"Charlie","email":null,"profile":{"age":null,"location":{"city":"Seattle","zip":"98101"},"skills":[]},"projects":[],"tags":["remote","contract"]}]
```

### Sample Output

```typescript
export interface Location {
  city: string;
  zip?: string;
}

export interface Metadata {
  score?: number;
  verified: boolean;
}

export interface Profile {
  age: null | number;
  experience?: number;
  location: Location;
  skills: string[];
}

export interface Projects {
  budget?: number;
  completed: boolean;
  title: string;
}

export interface CompanyData {
  email?: null | string;
  id: number | string;
  metadata?: Metadata | null;
  name: string;
  profile: Profile;
  projects: Projects[];
  tags?: string[];
}
```

---

## How to Run

Clone the repository:

```bash
git clone https://github.com/your-username/json-to-typescript-type-generator.git
```

Move into the project directory:

```bash
cd json-to-typescript-type-generator
```

Run the script:

```bash
python solution.py
```

Provide input through **stdin**.

---

## Concepts Used

- Recursive Parsing
- Schema Merging
- Type Inference
- Tree Traversal
- Deterministic Naming
- Interface Collision Resolution
- String Formatting

---

## Use Cases

- Automatically generating TypeScript interfaces from JSON
- Backend to frontend schema conversion
- Rapid API prototyping
- JSON schema inspection
- Type-safe frontend development

---

## License

This project is intended for educational and problem-solving purposes.
