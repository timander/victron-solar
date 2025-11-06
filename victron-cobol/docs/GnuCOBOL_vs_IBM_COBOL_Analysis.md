# GnuCOBOL 4 vs IBM COBOL (IMS Environment)

This document compares **GnuCOBOL 4** with **IBM COBOL for z/OS** (especially in IMS or CICS environments), focusing on transaction boundaries, DB2 z/OS integration, and assembly program invocation.

---

## 🧾 1. Transaction Boundaries

### IBM COBOL in IMS / CICS

IBM COBOL is designed to operate within a transaction-processing (TP) monitor such as **IMS TM** or **CICS**.  
That environment provides **ACID transaction control** across message queues, DL/I or DB2 calls, and other resources.

**Example (IMS or CICS context):**
```cobol
EXEC CICS SYNCPOINT END-EXEC
EXEC CICS SYNCPOINT ROLLBACK END-EXEC
```
or in IMS:
```cobol
CALL "CBLTDLI" USING GU  PCB-MASK  IO-AREA.
CALL "CBLTDLI" USING CHKP IO-AREA.
```

- **IMS handles transaction demarcation.** Each input message or GU (Get Unique) is a transaction start, and a `CHKP` or program termination ends or commits it.  
- **CICS handles via SYNCPOINT**, often tied to DB2 or DL/I under two-phase commit.

IBM’s COBOL runtime cooperates with the TP monitor so that:
- If you issue `SYNCPOINT`, it coordinates with DB2 and IMS.
- If an abend or rollback occurs, all resources are rolled back together.
- Logging and recovery are handled by the subsystem.

**In short:** IBM COBOL doesn’t manage the transaction; the subsystem does, and the compiler/runtime emits code that participates in that protocol.

---

### GnuCOBOL

GnuCOBOL has **no built-in transaction monitor**. There’s no concept of CHKP, SYNCPOINT, or rollback tied to a subsystem.

- The runtime executes as a simple process under the host OS.
- File I/O and SQL (if used via ODBC or embedded SQL) are committed or rolled back according to the host database’s semantics.
- You manage transactions *manually* via SQL:
  ```cobol
  EXEC SQL
     COMMIT WORK
  END-EXEC
  ```
  or 
  ```cobol
  EXEC SQL
     ROLLBACK WORK
  END-EXEC
  ```
- No XA or two-phase commit integration with message queues or other systems.

**Bottom line:**  
In IBM COBOL under IMS/CICS, transactions are part of the system fabric.  
In GnuCOBOL, they’re purely database-level (or none at all).

---

## 🗄️ 2. DB2 for z/OS Integration

### IBM COBOL

IBM COBOL tightly integrates with **DB2 for z/OS** using the **DB2 precompiler (DSNHPC)**.

**Flow:**
1. Source contains `EXEC SQL` statements.
2. The DB2 precompiler expands these into CALLs to DB2 runtime modules and generates a “DBRM” (Database Request Module).
3. The DBRM is bound into a DB2 package or plan.
4. The COBOL program is compiled and linked with DB2 stub modules (e.g., DSNHLI).

**Example:**
```cobol
EXEC SQL
   SELECT FIRSTNAME, LASTNAME
     INTO :WS-FNAME, :WS-LNAME
     FROM EMPLOYEE
    WHERE EMPNO = :WS-EMPNO
END-EXEC.
```

This goes through the DB2 precompiler to become CALLs to DSNHLI (the DB2 API stub).  
DB2 handles **cursor management, host variable binding, error codes, and transaction participation**.

**Key advantages:**
- Runs inside a single LUW (Logical Unit of Work) with IMS/CICS.
- DB2 participates in coordinated commits/rollbacks.
- Fully supported by IBM’s recovery, logging, and RACF-based security.

---

### GnuCOBOL

GnuCOBOL has **no native DB2 precompiler**. Options include:

- Using **embedded SQL via ODBC** with a driver for DB2 LUW or Db2 Connect.
- Using **EXEC SQL** with a third-party preprocessor (e.g., from OpenCOBOL-ESQL or Micro Focus if ported).
- Using plain **CALL “db2api”** or shell out to `db2cli`.

There’s **no automatic creation of DBRMs or plan binding**, and no integration with IMS/CICS for commit coordination.

So you can connect to DB2 **as a remote SQL client**, but not as a **TP participant**.

**Summary:**

| | **IBM COBOL for z/OS** | **GnuCOBOL 4** |
|--|--|--|
| Precompiler | DSNHPC | none |
| Binding | DBRM + PLAN | manual SQL or ODBC |
| Commit Control | IMS/CICS coordinated | host DB only |
| Authentication | RACF / z/OS credentials | ODBC / CLI credentials |
| Typical Scope | Server-side on z/OS | Client or mid-tier process |

---

## ⚙️ 3. Invoking Assembly Programs

### IBM COBOL

IBM COBOL routinely links to **Assembler (HLASM)** programs, both statically and dynamically.  

#### Static Linkage
- You `CALL 'PGMNAME' USING …`
- The Assembler routine is link-edited into the load module.
- Parameters are passed by address, following standard linkage conventions (register 1 points to a parameter list of addresses).

**Assembler entry example:**
```
COBOL → CALL 'PGMNAME' USING WS-BLOCK
Assembler entry:
  USING *,15
  L R1,0(,R1)   ; parameter list
  L R2,0(R1)    ; address of WS-BLOCK
```

Assembler routines can:
- Access control blocks (TCBs, PSBs, etc.)
- Invoke SVCs
- Manipulate registers and memory directly

**Because IBM COBOL runs in LE (Language Environment):**
- The linkage conventions are standardized (LE-conformant).
- RETURN-CODE and ABEND behaviors are interoperable.

You can even call back into COBOL from Assembly.

---

### GnuCOBOL

In GnuCOBOL, linkage to external routines is done through the **C ABI**.

- COBOL → C is straightforward (it compiles to C).
- COBOL → Assembly is possible but must adhere to the platform’s C calling convention.

Example:
```cobol
CALL "add_numbers" USING BY VALUE A B RETURNING C.
```
If you compile:
```c
int add_numbers(int a, int b) { return a + b; }
```
and link it, that works fine.

But:
- There’s no z/OS-style register protocol.
- No access to control blocks or SVCs.
- No LE environment.

So you can link with Assembly, but only **as a standard C ABI** on your host OS, not as a z/OS subroutine.

---

## 🧠 Summary Table

| Feature | **IBM COBOL (IMS/DB2)** | **GnuCOBOL 4** |
|----------|--------------------------|----------------|
| **Transaction Boundaries** | Managed by IMS/CICS (SYNCPOINT, CHKP, rollback integrated) | No TP monitor; only SQL commit/rollback |
| **DB2 Integration** | Native DB2 precompiler (DSNHPC), DBRM/PLAN binding, 2PC | No precompiler; ODBC or CLI access only |
| **Assembly Calls** | Full LE/HLASM interoperability, static/dynamic linking | Can call C or assembly via host ABI, not LE |
| **Commit Coordination** | IMS/CICS ↔ DB2 two-phase commit | None (per-connection only) |
| **Runtime Context** | z/OS LE + IMS/CICS + RACF | Host OS runtime (POSIX/Win32) |
| **Use Case** | Transactional mainframe workloads | Portability, modernization, or learning |

---
