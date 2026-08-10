# Plantilla de tarjeta de referencia

Usa esta base estructural para crear un archivo de tarjeta en `references/`. Para las reglas de
construcción, consulta la [Anatomía de una skill](./skill-anatomy.md).

## Esqueleto

````markdown
---
title: <Título de la regla>
impact: <CRITICAL | HIGH | MEDIUM-HIGH | MEDIUM | LOW-MEDIUM>
impactDescription: <Consecuencia o alcance breve>
tags: <lowercase-kebab-case>, <lowercase-kebab-case>
---

## <Título de la regla>

<Párrafo normativo que define la regla y por qué es importante.>

**Incorrecto (<descripción específica de cómo se infringe la regla>):**

```<lenguaje>
<Código que infringe la regla>
```

**Correcto (<descripción específica de cómo se aplica la regla>):**

```<lenguaje>
<Código que aplica la regla>
```

<!-- Añade subsecciones o ejemplos complementarios solo cuando la regla lo requiera. -->

Referencia: [<Fuente oficial>](https://example.com)
````
