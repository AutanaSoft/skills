# AutanaSoft SDD Lifecycle

**Versión 1.1.0** AutanaSoft Mayo 2026

> **Nota:** Este documento está pensado principalmente para agentes y LLMs que crean, actualizan,
> implementan, verifican o archivan artefactos SDD. Las reglas fuente viven en `rules/`.

---

## Resumen

Prácticas de lifecycle para artefactos Spec-Driven Development en proyectos AutanaSoft. Mantiene
artefactos SDD como documentos vivos, preserva decisiones aprobadas, exige phase gates y requiere
cleanup cuando una implementación reemplaza comportamiento existente.

---

## Índice

1. [Lifecycle](#1-lifecycle) — **HIGH**
   - 1.1
     [Tratar artefactos SDD como documentos vivos](#11-tratar-artefactos-sdd-como-documentos-vivos)
   - 1.2 [Usar statuses, versionado y changelog](#12-usar-statuses-versionado-y-changelog)
2. [Phase Gates](#2-phase-gates) — **HIGH**
   - 2.1
     [Respetar phase gates, aprobación y evidencia](#21-respetar-phase-gates-aprobación-y-evidencia)
3. [Apply Discipline](#3-apply-discipline) — **HIGH**
   - 3.1
     [Limpiar código obsoleto al reemplazar comportamiento](#31-limpiar-código-obsoleto-al-reemplazar-comportamiento)
4. [Validation](#4-validation) — **MEDIUM**
   - 4.1 [Respetar política de idioma y validación](#41-respetar-política-de-idioma-y-validación)

---

## 1. Lifecycle

**Impacto: HIGH**

Creación, actualización, preservación, versionado, frontmatter y changelog de artefactos SDD.

### 1.1 Tratar Artefactos SDD Como Documentos Vivos

**Impacto: HIGH — Evita perder decisiones aprobadas o regenerar artefactos inconsistentes.**

- Si un artefacto ya existe, leerlo antes de editar.
- Preservar decisiones aprobadas y actualizar solo las secciones afectadas.
- No sobrescribir ni recrear contenido válido de forma ciega.
- Actualizar frontmatter cuando exista y agregar una entrada en `Change Log`.
- Mantener consistentes PRD, spec, design, tasks, apply-progress y verify relacionados.

Referencia: `rules/lifecycle-living-artifacts.md`

### 1.2 Usar Statuses, Versionado Y Changelog

**Impacto: HIGH — Mantiene trazabilidad y aclara qué artefactos son fuente de verdad.**

- Usar statuses de lifecycle como `draft`, `approved`, `implemented`, `verified`, `archived` y
  `superseded`.
- Usar versionado semántico para documentos.
- Incluir frontmatter en artefactos gestionados cuando corresponda.
- Agregar filas de changelog sin borrar historial.

Referencia: `rules/lifecycle-versioning-status.md`

---

## 2. Phase Gates

**Impacto: HIGH**

Phase gates, aprobación de implementación, evidencia apply/verify y Strict TDD.

### 2.1 Respetar Phase Gates, Aprobación Y Evidencia

**Impacto: HIGH — Evita implementar desde drafts y verifica trabajo con evidencia real.**

- Antes de Apply, leer PRD, spec, design y tasks actuales.
- No implementar desde artefactos `draft` o `reviewed` sin aprobación explícita.
- Actualizar statuses y changelogs al mover artefactos a implementación.
- La evidencia Strict TDD debe registrar RED, GREEN, TRIANGULATE, SAFETY NET, REFACTOR y comandos
  cuando aplique.

Referencia: `rules/phase-approval-and-evidence.md`

---

## 3. Apply Discipline

**Impacto: HIGH**

Reglas para implementar desde SDD tasks, reemplazar código y limpiar deuda obsoleta.

### 3.1 Limpiar Código Obsoleto Al Reemplazar Comportamiento

**Impacto: HIGH — Evita deuda técnica, UI duplicada y paths muertos después de aplicar cambios.**

- Identificar código previo superseded por el cambio.
- Remover markup, componentes, helpers, imports y wiring reemplazados.
- Consolidar lógica duplicada de mapping o transformación.
- Actualizar tests, stories, fixtures o referencias que apunten a estructuras obsoletas.
- No ocultar código reemplazado con CSS, flags temporales o conditionals sin justificación
  explícita.

Referencia: `rules/apply-cleanup-replaced-code.md`

---

## 4. Validation

**Impacto: MEDIUM**

Política de idioma, comandos de validación y expectativas operativas.

### 4.1 Respetar Política De Idioma Y Validación

**Impacto: MEDIUM — Mantiene documentación consistente y evita validación costosa no solicitada.**

- Comunicar con el usuario en español.
- Escribir artefactos SDD, documentación técnica, documentación de producto, comentarios, JSDoc y
  código en inglés salvo pedido explícito contrario.
- Hacer una pregunta por vez cuando se requiere aclaración.
- Ejecutar validación relevante al workspace afectado.
- No ejecutar build salvo que el usuario lo pida explícitamente.

Referencia: `rules/language-and-validation.md`

---

## Autoría De Reglas

Toda regla nueva debe seguir `rules/_template.md` y usar una sección definida en
`rules/_sections.md`.
