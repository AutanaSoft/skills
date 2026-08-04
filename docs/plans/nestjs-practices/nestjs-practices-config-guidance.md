# Plan de corrección — Reglas `config-` de `nestjs-practices`

## 1. Objetivo

Corregir la implementación reciente de las reglas `config-` de `nestjs-practices` sin modificar la
arquitectura general ya aprobada.

El trabajo debe resolver específicamente:

1. Referencias nominales a otra skill dentro de `nestjs-practices`.
2. Pérdida del patrón explícito de:

   - factory nombrada;
   - factory exportada;
   - registro mediante `registerAs`;
   - constante registrada;
   - `export default`.

3. Uso accidental de `z.object(...).readonly()`, que impone congelamiento en runtime.
4. Descripción incompleta del dominio `config-` en README.
5. Falta de evidencia verificable de validaciones y evals posteriores al cambio.

La corrección no debe reabrir las decisiones conceptuales ya aceptadas sobre ownership, namespaces,
application contexts, fuentes externas, módulos dinámicos o secretos.

---

## 2. Rama de trabajo

La corrección debe realizarse en una rama nueva creada desde la rama principal actualizada.

### Nombre recomendado

```text
fix/nestjs-practices-config-guidance
```

El nombre refleja que se trata de una corrección localizada sobre la documentación y las reglas de
configuración de `nestjs-practices`.

### Preparación

```bash
git switch main
git pull --ff-only
git switch -c fix/nestjs-practices-config-guidance
```

Antes de editar:

```bash
git status
```

La implementación debe detenerse si existen cambios locales no relacionados que puedan
sobrescribirse o mezclarse accidentalmente.

No se debe hacer commit, push ni abrir pull request salvo solicitud explícita del usuario.

---

## 3. Requisitos previos obligatorios

Antes de modificar cualquier archivo:

1. Leer `AGENTS.md`.
2. Cargar la skill global:

```text
~/.agents/skills/skill-creator
```

1. Leer nuevamente:

   - `docs/skill-authoring/skill-anatomy.md`;
   - `docs/skill-authoring/skill-template.md`;
   - `docs/skill-authoring/reference-card-template.md`.

2. Leer el estado actual completo de:

   - `skills/typescript/nestjs-practices/SKILL.md`;
   - `skills/typescript/nestjs-practices/README.md`;
   - todas las tarjetas `references/config-*.md`.

3. Confirmar que la rama parte del commit que contiene la implementación inicial o de un estado
   posterior que la incluya.
4. Revisar el diff antes de sobrescribir cualquier archivo.

Las instrucciones actuales de `skill-creator` deben prevalecer sobre este plan cuando regulen
autoría, triggering, evals o validación.

---

## 4. Archivos que deben modificarse

```text
skills/typescript/nestjs-practices/
├── SKILL.md
├── README.md
└── references/
    ├── config-build-and-validate-namespaced-configuration.md
    ├── config-validate-dynamic-module-options.md
    └── config-avoid-hardcoded-secrets.md
```

También deberán revisarse, aunque no necesariamente modificarse:

```text
skills/typescript/nestjs-practices/references/config-inject-namespaced-configuration.md
skills/typescript/nestjs-practices/references/config-isolate-external-configuration-sources.md
skills/typescript/nestjs-practices/evals/
```

No deben crearse nuevas tarjetas `config-`.

No deben restaurarse las tarjetas antiguas que ya fueron fusionadas o renombradas.

---

## 5. Corrección 1 — Eliminar dependencias nominales entre skills

## Problema de la factory implícita

`nestjs-practices/SKILL.md` menciona directamente `nestjs-e2e-practices`.

Esto introduce una dependencia externa no garantizada:

- la otra skill puede no estar instalada;
- puede distribuirse por separado;
- puede cambiar de nombre;
- el consumidor puede no querer usarla;
- el activador deja de ser autosuficiente.

Una skill debe declarar sus propios límites sin asumir la existencia de otra.

## Archivo de la tarjeta consolidada

```text
skills/typescript/nestjs-practices/SKILL.md
```

## Cambios requeridos

Eliminar referencias nominales a:

```text
nestjs-e2e-practices
```

de:

- `description`;
- `Activation Contract`;
- cualquier otra sección task-time.

Sustituirlas por exclusiones autosuficientes.

### Frontmatter recomendado

```yaml
---
name: nestjs-practices
description: >
  Apply NestJS practices for modules, services, repositories, dependency injection, configuration
  with @nestjs/config, namespaced registerAs factories, application-context registration, typed
  injection, dynamic module options, external configuration sources, bootstrap, logging and errors,
  external contracts, data integration, and standalone application contexts. Use this skill when
  organizing NestJS configuration, reviewing @nestjs/config usage, creating typed configuration
  namespaces, separating worker and API configuration, validating dynamic module options, isolating
  process.env access, handling secrets, or performing broader NestJS architecture and runtime work.
  Do not use for end-to-end test design, test-runner orchestration, E2E fixtures, or E2E
  infrastructure lifecycle.
license: MIT
metadata:
  author: AutanaSoft
  version: '0.4.0'
---
```

La versión solo debe cambiar si la convención del repositorio exige versionar esta corrección.

### Activation Contract recomendado

```markdown
## Activation Contract

- Load this skill for NestJS modules, services, repositories, dependency injection, configuration,
  bootstrap, logging and errors, external contracts, data integration, or standalone application
  contexts.
- Do not load it for end-to-end test design, test-runner orchestration, E2E fixtures, or E2E
  infrastructure lifecycle.
- Do not activate it for generic TypeScript work that has no NestJS-specific decision.
```

## README

Eliminar también cualquier frase como:

```markdown
Use the separate `nestjs-e2e-practices` skill for end-to-end testing guidance.
```

Sustituir por:

```markdown
End-to-end testing conventions are outside this catalog's scope.
```

## Verificación

```bash
rg "nestjs-e2e-practices" skills/typescript/nestjs-practices
```

Resultado esperado:

```text
sin coincidencias
```

La ausencia debe verificarse en todo el directorio de la skill, no solo en `SKILL.md`.

---

## 6. Corrección 2 — Recuperar la factory nombrada y el registro explícito

## Problema del congelamiento runtime

La tarjeta consolidada actual usa:

```typescript
export default registerAs('payments', () => {
  // ...
});
```

Aunque esta forma es válida para NestJS, elimina el patrón explícito que existía anteriormente:

1. schema;
2. tipo;
3. factory nombrada;
4. `registerAs`;
5. constante registrada;
6. default export.

La omisión no fue una decisión aprobada.

## Archivo de la tarjeta de opciones dinámicas

```text
skills/typescript/nestjs-practices/references/config-build-and-validate-namespaced-configuration.md
```

## Cambio normativo

Añadir una instrucción explícita equivalente a:

```markdown
Export a named factory that constructs and validates the complete namespace. Register that factory
with `registerAs` under a stable semantic namespace, assign the registered configuration to a named
constant, and export the registered namespace as the module default.
```

La tarjeta debe explicar que esta separación:

- identifica claramente el boundary de construcción;
- diferencia construcción de registro;
- mantiene el namespace visible;
- facilita reutilización e inspección;
- conserva un patrón uniforme entre archivos de configuración;
- permite que otros archivos importen el namespace registrado mediante default import.

La justificación no debe centrarse en testing.

## Ejemplo incorrecto

Puede mantenerse un ejemplo inline, pero debe señalar también la pérdida del boundary explícito:

```typescript
import { registerAs } from '@nestjs/config';

export default registerAs('payments', () => ({
  apiUrl: process.env.PAYMENTS_API_URL,
  timeoutMs: process.env.PAYMENTS_TIMEOUT_MS || 5_000,
}));
```

Problemas que debe identificar:

- factory anónima;
- objeto potencialmente parcial;
- truthiness para defaults;
- ausencia de validación final;
- registro y construcción acoplados;
- contrato final no explícito.

## Ejemplo correcto propuesto

```typescript
import { registerAs } from '@nestjs/config';
import { z } from 'zod';

const paymentsConfigSchema = z.object({
  apiUrl: z.string().url(),
  timeoutMs: z.number().int().positive(),
  requestPath: z.string().startsWith('/'),
  endpoint: z.string().url(),
});

export type PaymentsConfig = Readonly<z.infer<typeof paymentsConfigSchema>>;

export const paymentsConfigFactory = (): PaymentsConfig => {
  const apiUrlOverride = process.env.PAYMENTS_API_URL;
  const timeoutOverride = process.env.PAYMENTS_TIMEOUT_MS;
  const pathOverride = process.env.PAYMENTS_PATH;

  const apiUrl = apiUrlOverride === undefined ? undefined : apiUrlOverride.trim();

  const timeoutMs = timeoutOverride === undefined ? 5_000 : Number(timeoutOverride);

  const requestPath = pathOverride === undefined ? '/v1/payments' : pathOverride.trim();

  const candidate = {
    apiUrl,
    timeoutMs,
    requestPath,
    endpoint: apiUrl === undefined ? undefined : `${apiUrl.replace(/\/$/, '')}${requestPath}`,
  };

  return paymentsConfigSchema.parse(candidate);
};

const paymentsConfig = registerAs<PaymentsConfig>('payments', paymentsConfigFactory);

export default paymentsConfig;
```

## Contrato requerido

El ejemplo debe conservar todos estos elementos:

```text
paymentsConfigSchema
PaymentsConfig
paymentsConfigFactory
registerAs<PaymentsConfig>('payments', paymentsConfigFactory)
const paymentsConfig
export default paymentsConfig
```

## Consideración sobre el generic de `registerAs`

Antes de fijar:

```typescript
registerAs<PaymentsConfig>;
```

se debe verificar que la versión de `@nestjs/config` compatible con el repositorio admite
correctamente esa firma.

Si la documentación oficial o la versión instalada recomiendan inferencia sin generic, se puede
usar:

```typescript
const paymentsConfig = registerAs('payments', paymentsConfigFactory);
```

La factory nombrada y el default export siguen siendo obligatorios aunque se omita el generic.

---

## 7. Corrección 3 — Eliminar congelamiento accidental de Zod

## Problema

Las tarjetas usan:

```typescript
z.object({...}).readonly()
```

En Zod, `.readonly()` no es solo una representación de tipo. Puede congelar el resultado en runtime.

La decisión aprobada estableció:

- inmutabilidad contractual mediante TypeScript;
- `Object.freeze` opcional;
- no imponer congelamiento runtime universalmente.

## Archivos afectados

```text
config-build-and-validate-namespaced-configuration.md
config-validate-dynamic-module-options.md
config-avoid-hardcoded-secrets.md
```

También revisar cualquier otra tarjeta `config-` que use:

```text
.readonly()
```

## Cambio requerido

Eliminar `.readonly()` de los schemas usados como ejemplos generales.

### Antes

```typescript
const schema = z
  .object({
    apiUrl: z.string().url(),
  })
  .readonly();
```

### Después

```typescript
const schema = z.object({
  apiUrl: z.string().url(),
});
```

Representar la inmutabilidad mediante el tipo:

```typescript
type Config = Readonly<z.infer<typeof schema>>;
```

o:

```typescript
interface Config {
  readonly apiUrl: string;
}
```

## Texto normativo recomendado

```markdown
Express configuration immutability through `Readonly<T>` or readonly properties. Do not require
runtime freezing. Use `Object.freeze` or a validator feature that freezes output only when the
project explicitly needs that runtime guarantee.
```

## Búsqueda de control

```bash
rg "\.readonly\(\)" skills/typescript/nestjs-practices/references/config-*.md
```

Resultado esperado:

- cero coincidencias; o
- coincidencias únicamente dentro de una explicación explícita sobre congelamiento runtime opcional.

No debe quedar `.readonly()` en ejemplos presentados como patrón predeterminado.

---

## 8. Corrección 4 — Ajustar la tarjeta de módulos dinámicos

## Archivo de la tarjeta de secretos

```text
skills/typescript/nestjs-practices/references/config-validate-dynamic-module-options.md
```

## Cambios requeridos para secretos

1. Eliminar `.readonly()` del schema.
2. Mantener separados:

   - input aceptado;
   - resultado validado;
   - token registrado.

3. Conservar `Readonly` en tipos TypeScript.
4. Mantener un validador compartido entre `forRoot` y `forRootAsync`.

## Ejemplo corregido de carga segura

```typescript
import { DynamicModule, Module } from '@nestjs/common';
import { z } from 'zod';

export const PAYMENTS_OPTIONS = Symbol('PAYMENTS_OPTIONS');

const paymentsModuleOptionsSchema = z.object({
  apiUrl: z.string().url(),
  timeoutMs: z.number().int().positive().default(5_000),
});

type PaymentsModuleOptionsInput = Readonly<z.input<typeof paymentsModuleOptionsSchema>>;

type PaymentsModuleOptions = Readonly<z.infer<typeof paymentsModuleOptionsSchema>>;

const validatePaymentsOptions = (options: PaymentsModuleOptionsInput): PaymentsModuleOptions => {
  return paymentsModuleOptionsSchema.parse(options);
};

@Module({})
export class PaymentsModule {
  static forRoot(options: PaymentsModuleOptionsInput): DynamicModule {
    const validatedOptions = validatePaymentsOptions(options);

    return {
      module: PaymentsModule,
      providers: [
        {
          provide: PAYMENTS_OPTIONS,
          useValue: validatedOptions,
        },
      ],
      exports: [PAYMENTS_OPTIONS],
    };
  }
}
```

Para `forRootAsync`, la tarjeta debe seguir indicando que la factory asíncrona pasa su resultado
por:

```typescript
validatePaymentsOptions(resolvedOptions);
```

antes de exponerlo.

No es necesario convertir la tarjeta en una implementación completa de `forRootAsync`.

---

## 9. Corrección 5 — Ajustar la tarjeta de secretos

## Archivo del README

```text
skills/typescript/nestjs-practices/references/config-avoid-hardcoded-secrets.md
```

## Cambios

1. Eliminar `.readonly()` del schema.
2. Mantener `Readonly` en el tipo de salida cuando el ejemplo exporte un contrato.
3. Conservar el error sanitizado.
4. Evitar que el ejemplo sugiera capturar cualquier error y reemplazarlo sin preservar causas cuando
   el proyecto necesite diagnóstico estructurado.
5. Aclarar que el ejemplo simplificado muestra el límite de exposición, no una política universal de
   error handling.

## Ejemplo corregido

```typescript
import { z } from 'zod';

const paymentsSchema = z.object({
  apiKey: z.string().min(1),
});

type PaymentsConfig = Readonly<z.infer<typeof paymentsSchema>>;

export function loadPaymentsConfig(): PaymentsConfig {
  const candidate = {
    apiKey: process.env.PAYMENTS_API_KEY,
  };

  try {
    return paymentsSchema.parse(candidate);
  } catch {
    throw new Error('Invalid payments configuration: PAYMENTS_API_KEY is missing or malformed');
  }
}
```

La tarjeta debe seguir prohibiendo:

- valores sensibles en errores;
- dumps de `process.env`;
- namespaces completos serializados;
- defaults como `'change-me'`;
- logs de objetos sin sanitizar.

---

## 10. Corrección 6 — Completar la descripción del dominio `config-`

## Archivo

```text
skills/typescript/nestjs-practices/README.md
```

## Problema del dominio resumido

La tabla de dominios resume `config-` solo como:

```text
Configuration placement, validation, and injection
```

El catálogo actual también cubre:

- ownership;
- construcción;
- registro por application context;
- fuentes externas;
- módulos dinámicos;
- secretos;
- diagnósticos seguros.

## Cambio propuesto

```markdown
| `config-` | Configuration ownership, construction, validation, registration, injection, external
sources, dynamic options, and secrets |
```

Si la línea resulta demasiado larga para el formato existente, puede usarse una versión más
compacta:

```markdown
| `config-` | NestJS configuration ownership, lifecycle, injection, external sources, and secrets |
```

La tabla detallada de tarjetas debe conservarse sin duplicar normativa.

---

## 11. Corrección 7 — Revisar coherencia de la tarjeta de inyección

## Archivo de revisión

```text
config-inject-namespaced-configuration.md
```

Probablemente no requiere modificación sustancial, pero se debe comprobar que:

- siga usando default import del namespace registrado;
- ese default import sea coherente con el patrón restaurado;
- `ConfigType<typeof paymentsConfig>` siga funcionando;
- la propiedad inyectada sea readonly;
- no se sugiera que Zod debe congelar el objeto.

Ejemplo esperado:

```typescript
import { Inject, Injectable } from '@nestjs/common';
import type { ConfigType } from '@nestjs/config';
import paymentsConfig from './config/payments.config';

@Injectable()
export class PaymentsClient {
  constructor(
    @Inject(paymentsConfig.KEY)
    private readonly config: Readonly<ConfigType<typeof paymentsConfig>>,
  ) {}
}
```

Debe existir coherencia directa entre:

```typescript
export default paymentsConfig;
```

y:

```typescript
import paymentsConfig from './config/payments.config';
```

---

## 12. Revisión de enlaces y ownership normativo

Después de editar, comprobar que:

- `SKILL.md` solo enrute;
- README solo inventaríe;
- la tarjeta consolidada posea factory y validación de namespace;
- la tarjeta de inyección posea consumo tipado;
- la tarjeta de secretos posea confidencialidad y sanitización;
- la tarjeta de módulos dinámicos posea `forRoot` y `forRootAsync`;
- no se duplique normativa entre ellas.

Búsquedas recomendadas:

```bash
rg "registerAs" skills/typescript/nestjs-practices
```

```bash
rg "export const .*ConfigFactory" skills/typescript/nestjs-practices/references/config-*.md
```

```bash
rg "export default" skills/typescript/nestjs-practices/references/config-*.md
```

La tarjeta consolidada debe mostrar claramente los tres componentes:

```text
factory
registerAs
default export
```

---

## 13. Evaluación de triggering con `skill-creator`

Modificar el `description` obliga a repetir las evaluaciones de triggering.

## Casos positivos mínimos

La skill debe activarse para solicitudes como:

1. “Organiza la configuración de una aplicación NestJS.”
2. “Revisa nuestro uso de `@nestjs/config`.”
3. “Crea un namespace tipado para pagos.”
4. “Separa la configuración de una API y un worker.”
5. “Valida las opciones de un módulo dinámico NestJS.”
6. “Evita que los servicios accedan directamente a `process.env`.”
7. “Configura secretos externos en NestJS.”
8. “Revisa el registro con `ConfigModule.forRoot`.”

## Casos negativos mínimos

No debe activarse para:

1. unit tests genéricos;
2. Jest discovery;
3. orquestación E2E;
4. fixtures E2E;
5. lifecycle de bases temporales de pruebas;
6. TypeScript genérico sin NestJS;
7. configuración de otro framework;
8. black-box testing contra una API desplegada.

Los casos negativos deben describir el alcance excluido sin asumir que existe otra skill que lo
cubra.

## Evaluación de comportamiento

Comprobar que, ante una solicitud de namespace:

- exporta una factory nombrada;
- valida el objeto final;
- registra con `registerAs`;
- exporta por default el namespace registrado;
- usa inmutabilidad TypeScript;
- no usa `.readonly()` de Zod como patrón predeterminado;
- no impone `env.validation.ts`;
- no introduce reglas de testing.

---

## 14. Validación técnica

## Validación estructural

Ejecutar el comando real soportado por el repositorio. Como referencia:

```bash
python scripts/quick_validate.py skills/typescript/nestjs-practices
```

Si el script usa otra interfaz:

```bash
python scripts/quick_validate.py --help
```

y aplicar la forma documentada.

## Validación completa

```bash
pnpm validate
```

## Enlaces

Ejecutar las verificaciones de enlaces que formen parte de `pnpm validate` o de las herramientas del
repositorio.

Adicionalmente:

```bash
rg "config-place-files-under-src-config|config-use-namespaced-register-as-factories|config-validate-environment-with-zod|config-register-configuration-in-app-module|config-prevent-direct-environment-access"
```

Resultado esperado:

- sin referencias normativas activas;
- las apariciones dentro de planes históricos son aceptables si esos documentos preservan el
  historial.

## Referencias cruzadas entre skills

```bash
rg "nestjs-e2e-practices" skills/typescript/nestjs-practices
```

Resultado esperado:

```text
sin coincidencias
```

## Congelamiento runtime

```bash
rg "\.readonly\(\)" skills/typescript/nestjs-practices/references/config-*.md
```

Resultado esperado:

```text
sin usos normativos o ejemplos predeterminados
```

---

## 15. Revisión del diff

Antes de finalizar:

```bash
git diff --check
git diff --stat
git diff
```

Revisar específicamente que:

- no se hayan modificado tarjetas ajenas al alcance;
- no se hayan restaurado archivos antiguos;
- no se hayan introducido aliases;
- no se hayan añadido reglas de testing;
- no se haya modificado `nestjs-e2e-practices`;
- no se hayan agregado dependencias entre skills;
- los ejemplos sigan compilando conceptualmente;
- las líneas de Markdown respeten el formato del repositorio.

---

## 16. Orden recomendado de implementación

1. Crear la rama:

```text
fix/nestjs-practices-config-guidance
```

1. Leer `AGENTS.md` y cargar `skill-creator`.
2. Revisar el estado actual de todos los archivos afectados.
3. Eliminar referencias nominales a otras skills en `SKILL.md`.
4. Eliminar la referencia equivalente en README.
5. Recuperar factory nombrada, registro separado y default export en la tarjeta consolidada.
6. Eliminar `.readonly()` de los schemas Zod.
7. Ajustar la tarjeta de módulos dinámicos.
8. Ajustar la tarjeta de secretos.
9. Completar la descripción del dominio `config-` en README.
10. Revisar coherencia con la tarjeta de inyección.
11. Buscar referencias cruzadas y patrones obsoletos.
12. Ejecutar evals de triggering y comportamiento con `skill-creator`.
13. Ejecutar `quick_validate.py`.
14. Ejecutar `pnpm validate`.
15. Inspeccionar el diff completo.
16. Documentar resultados.
17. No hacer commit ni push sin autorización explícita.

---

## 17. Criterios de aceptación

- [ ] El trabajo se realizó en `fix/nestjs-practices-config-guidance`.
- [ ] Se cargó `~/.agents/skills/skill-creator`.
- [ ] `nestjs-practices` no menciona nominalmente ninguna otra skill.
- [ ] El activador declara límites E2E de forma autosuficiente.
- [ ] README no depende de otra skill.
- [ ] La tarjeta consolidada exporta una factory nombrada.
- [ ] La factory construye y valida el objeto final.
- [ ] La factory se registra mediante `registerAs`.
- [ ] El namespace registrado se asigna a una constante.
- [ ] El namespace se exporta como default.
- [ ] La tarjeta de inyección usa coherentemente ese default export.
- [ ] Los schemas Zod no usan `.readonly()` como patrón predeterminado.
- [ ] La inmutabilidad se expresa mediante `Readonly<T>` o propiedades readonly.
- [ ] Runtime freezing permanece opcional.
- [ ] La descripción de `config-` en README cubre el dominio actual.
- [ ] No se añadieron reglas de testing.
- [ ] No se modificó la skill E2E.
- [ ] No existen referencias a tarjetas obsoletas.
- [ ] Los enlaces relativos resuelven.
- [ ] Las evals positivas y negativas de triggering pasan.
- [ ] Las evaluaciones de comportamiento conservan el patrón explícito de factory.
- [ ] `quick_validate.py` pasa.
- [ ] `pnpm validate` pasa.
- [ ] `git diff --check` pasa.
- [ ] El diff fue revisado manualmente.
- [ ] No se hizo commit ni push sin autorización.

---

## 18. Entrega esperada

Al terminar la ejecución, reportar:

1. Nombre de la rama.
2. Archivos modificados.
3. Referencias nominales eliminadas.
4. Ejemplo final de factory, `registerAs` y default export.
5. Usos de `.readonly()` eliminados.
6. Resultado de las evals de triggering.
7. Resultado de las evals de comportamiento.
8. Resultado de `quick_validate.py`.
9. Resultado de `pnpm validate`.
10. Resultado de `git diff --check`.
11. Gaps o verificaciones no ejecutadas.
12. Estado de commit y push.

---

## 19. Resumen operativo

```text
update main
  → create fix/nestjs-practices-config-guidance
  → load skill-creator
  → remove cross-skill references
  → restore named factory
  → separate registerAs and default export
  → remove Zod runtime readonly
  → complete README scope
  → review typed injection
  → rerun triggering and behavior evals
  → run quick validation
  → run pnpm validate
  → inspect diff
```
