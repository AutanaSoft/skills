# Plan de implementación — Actualización de reglas `config-` en `nestjs-practices`

## 1. Objetivo

Actualizar las reglas con prefijo `config-` de la skill `nestjs-practices` para que representen un
modelo coherente, no duplicado y portable de configuración en NestJS mediante `@nestjs/config`.

La implementación debe aplicar el registro de decisiones aprobado y respetar el modelo de autoría
del repositorio:

- `SKILL.md` funciona como punto de entrada, activación y navegación.
- Las reglas normativas, excepciones, ejemplos y fuentes viven en `references/`.
- `README.md` funciona como inventario y guía de mantenimiento.
- Las tarjetas relacionadas se enlazan; no duplican normativa.
- Cada tarjeta representa una regla principal o una decisión cohesiva.
- Las reglas de testing quedan fuera del dominio `config-`.

Este documento es un plan de implementación. No modifica todavía el repositorio.

## 2. Requisito obligatorio: usar `skill-creator`

Antes de editar cualquier archivo de la skill se debe cargar la skill global:

```text
~/.agents/skills/skill-creator
```

La implementación deberá seguir las instrucciones vigentes de `skill-creator` para modificar una
skill existente, especialmente en lo relativo a:

- contrato de frontmatter;
- calidad de los triggers de activación;
- disciplina de carga progresiva de referencias;
- separación entre `SKILL.md`, tarjetas y README;
- evaluación del comportamiento con y sin la skill;
- validación e inspección final.

No se debe asumir el contenido de `skill-creator` a partir de memoria. Debe leerse en el momento de
la implementación y sus instrucciones actuales prevalecerán sobre este plan cuando regulen el
proceso de autoría.

Además, se deben respetar las reglas del repositorio en `AGENTS.md`. En particular:

1. Cargar `skill-creator` antes de modificar la skill.
2. Confirmar que la descripción de `nestjs-practices` conserva triggers suficientes.
3. Usar `scripts/quick_validate.py`.
4. Ejecutar `pnpm validate`.
5. No realizar commit ni push salvo solicitud explícita.
6. Mantener documentación, tarjetas y ejemplos en inglés profesional y neutral.

## 3. Fuentes normativas del cambio

La implementación deberá trabajar con estas fuentes, en este orden:

1. `AGENTS.md`.
2. Skill global `~/.agents/skills/skill-creator`.
3. Registro de decisiones aprobado para las reglas `config-`.
4. `docs/skill-authoring/skill-anatomy.md`.
5. `docs/skill-authoring/skill-template.md`.
6. `docs/skill-authoring/reference-card-template.md`.
7. Estado actual de:
   - `skills/typescript/nestjs-practices/SKILL.md`;
   - `skills/typescript/nestjs-practices/README.md`;
   - todas las tarjetas `references/config-*.md`.
8. Documentación oficial de NestJS y de las APIs utilizadas en ejemplos.

Antes de escribir, se debe volver a leer el contenido actual de todos los archivos afectados para no
sobrescribir cambios posteriores o intencionales.

## 4. Resultado esperado

Al finalizar, `nestjs-practices` deberá presentar un conjunto de reglas `config-` con estas
propiedades:

- La configuración se organiza según ownership y arquitectura, no mediante una ruta universal.
- Cada namespace construye su configuración completa.
- Defaults, overrides, transformaciones y valores derivados siguen una precedencia explícita.
- La configuración final se valida una sola vez en su boundary de construcción.
- La normativa es agnóstica respecto de la librería de validación.
- Los ejemplos usan Zod de forma consistente.
- La validación global es opcional y complementaria.
- Cada application context registra únicamente la configuración que necesita.
- Los consumidores reciben contratos tipados e inmutables mediante inyección.
- El acceso a `process.env` y a otras fuentes externas queda encapsulado.
- Los módulos dinámicos validan sus opciones en `forRoot` o `forRootAsync`.
- Los secretos pueden provenir de proveedores externos y nunca se exponen en errores o logs.
- Las tarjetas no contienen reglas de unit testing, integración ni E2E.
- `SKILL.md` y `README.md` no duplican el contenido normativo de las tarjetas.

## 5. Árbol de archivos objetivo

```text
skills/
└── typescript/
    └── nestjs-practices/
        ├── SKILL.md
        ├── README.md
        └── references/
            ├── config-locate-configuration-by-ownership.md
            ├── config-build-and-validate-namespaced-configuration.md
            ├── config-register-configuration-per-application-context.md
            ├── config-inject-namespaced-configuration.md
            ├── config-isolate-external-configuration-sources.md
            ├── config-validate-dynamic-module-options.md
            └── config-avoid-hardcoded-secrets.md
```

Este árbol mantiene siete tarjetas, pero reorganiza su responsabilidad:

- dos tarjetas actuales se fusionan;
- varias tarjetas se renombran para representar mejor su regla;
- se incorpora una tarjeta específica para opciones de módulos dinámicos;
- la tarjeta de secretos permanece independiente por su impacto de seguridad.

No se debe crear ninguna tarjeta `config-test-*`.

## 6. Mapa de migración de tarjetas

| Estado actual                                    | Acción                               | Estado objetivo                                            |
| ------------------------------------------------ | ------------------------------------ | ---------------------------------------------------------- |
| `config-place-files-under-src-config.md`         | Renombrar y reescribir               | `config-locate-configuration-by-ownership.md`              |
| `config-use-namespaced-register-as-factories.md` | Fusionar                             | `config-build-and-validate-namespaced-configuration.md`    |
| `config-validate-environment-with-zod.md`        | Fusionar y eliminar archivo anterior | `config-build-and-validate-namespaced-configuration.md`    |
| `config-register-configuration-in-app-module.md` | Renombrar y reescribir               | `config-register-configuration-per-application-context.md` |
| `config-inject-namespaced-configuration.md`      | Conservar y actualizar               | `config-inject-namespaced-configuration.md`                |
| `config-prevent-direct-environment-access.md`    | Renombrar y ampliar                  | `config-isolate-external-configuration-sources.md`         |
| No existe                                        | Crear                                | `config-validate-dynamic-module-options.md`                |
| `config-avoid-hardcoded-secrets.md`              | Conservar y ampliar                  | `config-avoid-hardcoded-secrets.md`                        |

La eliminación de archivos antiguos y la actualización de todos sus enlaces debe ocurrir en la misma
unidad de trabajo para no dejar referencias rotas.

## 7. Fases de implementación

### Fase 0 — Preparación y control de cambios

1. Leer `AGENTS.md` completo.
2. Cargar `~/.agents/skills/skill-creator`.
3. Leer `skill-anatomy.md`, `skill-template.md` y `reference-card-template.md`.
4. Leer `SKILL.md`, `README.md` y todas las tarjetas `config-*` actuales.
5. Revisar el estado de Git para detectar cambios locales.
6. Tratar cualquier diferencia no generada durante esta implementación como intencional.
7. Verificar documentación oficial y versión de `@nestjs/config` antes de afirmar APIs no triviales.
8. Identificar todos los enlaces entrantes a tarjetas que serán eliminadas o renombradas.

### Fase 1 — Reestructurar el catálogo

1. Crear la tarjeta consolidada de construcción y validación.
2. Reescribir y renombrar ubicación, registro y fuentes externas.
3. Actualizar inyección.
4. Crear la tarjeta de módulos dinámicos.
5. Actualizar secretos.
6. Eliminar tarjetas reemplazadas después de migrar su contenido válido.
7. Actualizar enlaces relativos entre tarjetas.

No copiar secciones normativas entre tarjetas. Cuando una decisión pertenezca a otra tarjeta,
enlazarla.

### Fase 2 — Actualizar `SKILL.md`

- Mantener frontmatter salvo que `skill-creator` demuestre que los triggers requieren ajuste.
- Confirmar que `name` siga coincidiendo con `nestjs-practices`.
- Conservar triggers para arquitectura NestJS, `@nestjs/config`, namespaces, registro, inyección,
  secretos y módulos dinámicos.
- Actualizar `Quick Reference` con las nuevas tarjetas.
- Eliminar referencias a tarjetas retiradas.
- Mantener normativa, ejemplos y excepciones fuera de `SKILL.md`.

Ejemplo de índice:

```markdown
## Quick Reference

- Locate configuration by architectural ownership — `config-locate-configuration-by-ownership`
- Build and validate namespaced configuration — `config-build-and-validate-namespaced-configuration`
- Register configuration per application context —
  `config-register-configuration-per-application-context`
- Inject typed namespaced configuration — `config-inject-namespaced-configuration`
- Isolate external configuration sources — `config-isolate-external-configuration-sources`
- Validate dynamic module options — `config-validate-dynamic-module-options`
- Keep secrets out of source and diagnostics — `config-avoid-hardcoded-secrets`
```

### Fase 3 — Actualizar `README.md`

- Sustituir el inventario antiguo por las siete tarjetas objetivo.
- Registrar fusiones y renombres para mantenimiento.
- Revisar contadores y tablas de categorías.
- Mantener el README libre de normativa task-time.
- Confirmar que todas las rutas relativas existan.

Ejemplo:

```markdown
### Configuration

| Card                                                    | Purpose                                                           |
| ------------------------------------------------------- | ----------------------------------------------------------------- |
| `config-locate-configuration-by-ownership`              | Choose a location based on project conventions and ownership.     |
| `config-build-and-validate-namespaced-configuration`    | Build complete namespaces and validate their final shape.         |
| `config-register-configuration-per-application-context` | Load only the namespaces required by each application context.    |
| `config-inject-namespaced-configuration`                | Inject typed, read-only namespace contracts.                      |
| `config-isolate-external-configuration-sources`         | Keep consumers independent from environment and secret providers. |
| `config-validate-dynamic-module-options`                | Validate `forRoot` and `forRootAsync` inputs at registration.     |
| `config-avoid-hardcoded-secrets`                        | Prevent secret leakage in source, defaults, logs, and errors.     |
```

## 8. Diseño detallado de las tarjetas

Todas deben cumplir el template de reference cards:

- frontmatter válido;
- título idéntico al H2;
- impacto permitido;
- `impactDescription` presente;
- máximo cuatro tags lowercase kebab-case;
- ejemplo `Incorrect` y ejemplo `Correct` sobre la misma decisión;
- lenguaje declarado en todos los bloques;
- al menos una referencia HTTPS oficial;
- enlaces relativos en vez de normativa duplicada.

### 8.1 `config-locate-configuration-by-ownership.md`

Frontmatter propuesto:

```yaml
---
title: Locate configuration by architectural ownership
impact: MEDIUM
impactDescription:
  Keeps configuration discoverable without imposing a repository-wide folder that conflicts with
  project architecture.
tags: nestjs, configuration, architecture, file-organization
---
```

Debe establecer:

- respetar la convención del proyecto;
- usar `src/common/config` cuando `src/common` sea el hogar transversal;
- usar `src/config` solo como fallback;
- permitir configuración feature-owned dentro del módulo;
- mantener defaults junto a su owner;
- extraer defaults solo con reutilización real y ownership claro;
- evitar carpetas globales vagas.

Ejemplo correcto:

```text
src/
└── modules/
    └── payments/
        ├── payments.module.ts
        └── config/
            └── payments.config.ts
```

Debe enlazar a construcción y registro.

### 8.2 `config-build-and-validate-namespaced-configuration.md`

Frontmatter aprobado:

```yaml
---
title: Build and validate namespaced configuration
impact: HIGH
impactDescription:
  Prevents partial, inconsistent, or invalid runtime configuration from reaching application
  consumers.
tags: nestjs, configuration, validation, register-as
---
```

Responsabilidad:

- namespaces breves, estables y semánticos;
- coherencia entre archivo, namespace y tipo;
- construcción de configuración completa;
- propiedades defaulted, overridable, required y derived;
- precedencia defaults → overrides definidos → transformaciones/derivados → validación final;
- detección de presencia sin truthiness;
- validación autoritativa en la factory;
- normativa agnóstica y ejemplos con Zod;
- contratos `Readonly`;
- `env.validation.ts` opcional y complementario;
- exclusión de datos por request, estado de dominio y settings mutables.

Ejemplo incorrecto:

```typescript
import { registerAs } from '@nestjs/config';

export default registerAs('payments', () => ({
  apiUrl: process.env.PAYMENTS_API_URL,
  timeoutMs: process.env.PAYMENTS_TIMEOUT_MS,
}));
```

Ejemplo correcto:

```typescript
import { registerAs } from '@nestjs/config';
import { z } from 'zod';

const paymentsSchema = z
  .object({
    apiUrl: z.string().url(),
    timeoutMs: z.number().int().positive(),
    requestPath: z.string().startsWith('/'),
  })
  .readonly();

export type PaymentsConfig = Readonly<z.infer<typeof paymentsSchema>>;

export default registerAs('payments', (): PaymentsConfig => {
  const timeoutOverride = process.env.PAYMENTS_TIMEOUT_MS;

  const candidate = {
    apiUrl: process.env.PAYMENTS_API_URL,
    timeoutMs: timeoutOverride === undefined ? 5_000 : Number(timeoutOverride),
    requestPath: '/v1/payments',
  };

  return paymentsSchema.parse(candidate);
});
```

La validación global solo debe presentarse para reglas entre namespaces, globals compartidos,
reporte agregado o convención existente. No debe duplicar `paymentsSchema`.

### 8.3 `config-register-configuration-per-application-context.md`

Frontmatter propuesto:

```yaml
---
title: Register configuration per application context
impact: HIGH
impactDescription:
  Prevents unrelated applications, workers, and commands from sharing an oversized or incorrectly
  initialized configuration graph.
tags: nestjs, configuration, modules, application-context
---
```

Debe establecer:

- no asumir un único `AppModule`;
- contemplar HTTP apps, workers, CLI, cron y standalone contexts;
- cargar solo namespaces necesarios;
- reutilizar factories cuando corresponda;
- no imponer inicialización única para todo el monorepo;
- permitir `isGlobal: true` dentro del contexto, sin convertirlo en regla universal;
- validar dentro del contexto consumidor.

Ejemplos:

```typescript
@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      load: [appConfig, databaseConfig, paymentsConfig],
    }),
  ],
})
export class ApiAppModule {}
```

```typescript
@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      load: [databaseConfig, workerConfig],
    }),
  ],
})
export class PaymentsWorkerModule {}
```

### 8.4 `config-inject-namespaced-configuration.md`

Título preferido:

```yaml
title: Inject typed namespaced configuration
```

Debe establecer:

- preferir `config.KEY` y `ConfigType<typeof config>` para `registerAs`;
- permitir tokens tipados equivalentes;
- inyectar contratos read-only;
- no revalidar ni mutar en consumidores;
- reservar `ConfigService` para lookup dinámico o múltiples namespaces justificados;
- evitar strings dispersos como `payments.apiUrl`;
- separar settings mutables de la configuración de bootstrap.

Ejemplo correcto:

```typescript
import { Inject, Injectable } from '@nestjs/common';
import { ConfigType } from '@nestjs/config';
import paymentsConfig from './config/payments.config';

@Injectable()
export class PaymentsClient {
  constructor(
    @Inject(paymentsConfig.KEY)
    private readonly config: ConfigType<typeof paymentsConfig>,
  ) {}

  createRequest(): void {
    const { apiUrl, timeoutMs } = this.config;
  }
}
```

`Object.freeze` será opcional; la garantía estándar será de tipado.

### 8.5 `config-isolate-external-configuration-sources.md`

Frontmatter propuesto:

```yaml
---
title: Isolate external configuration sources
impact: HIGH
impactDescription:
  Prevents application consumers from coupling business logic to environment variables, secret
  providers, or deployment mechanisms.
tags: nestjs, configuration, dependency-injection, environment
---
```

Debe prohibir acceso directo desde consumidores a:

- `process.env`;
- Vault;
- AWS Secrets Manager;
- Azure Key Vault;
- Google Secret Manager;
- Kubernetes secret mounts;
- archivos o APIs de configuración externas.

El acceso debe quedar en factories, adaptadores, bootstrap o módulos dinámicos. Debe reconocer
fuentes asíncronas y no forzar `registerAs` síncrono cuando la arquitectura requiera `forRootAsync`
o providers asíncronos.

### 8.6 `config-validate-dynamic-module-options.md`

Frontmatter propuesto:

```yaml
---
title: Validate dynamic module options at registration
impact: HIGH
impactDescription:
  Prevents invalid public module options from reaching internal providers and failing later at
  runtime.
tags: nestjs, configuration, dynamic-modules, validation
---
```

Debe establecer:

- `forRoot(options)` valida antes de registrar providers;
- `forRootAsync(...)` valida el objeto ya resuelto;
- el módulo posee su contrato público;
- consumidores internos reciben opciones validadas;
- no se duplica validación;
- no se asume `process.env` como fuente;
- se exponen tokens y contratos read-only;
- normativa agnóstica con ejemplos Zod.

Ejemplo:

```typescript
import { DynamicModule, Module } from '@nestjs/common';
import { z } from 'zod';

const paymentsModuleOptionsSchema = z
  .object({
    apiUrl: z.string().url(),
    timeoutMs: z.number().int().positive().default(5_000),
  })
  .readonly();

type PaymentsModuleOptions = Readonly<z.infer<typeof paymentsModuleOptionsSchema>>;

@Module({})
export class PaymentsModule {
  static forRoot(options: PaymentsModuleOptions): DynamicModule {
    const validatedOptions = paymentsModuleOptionsSchema.parse(options);

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

### 8.7 `config-avoid-hardcoded-secrets.md`

Puede conservar el nombre de archivo para minimizar enlaces rotos. Título preferido:

```yaml
title: Keep secrets out of source and diagnostics
```

Frontmatter propuesto:

```yaml
impact: CRITICAL
impactDescription:
  Prevents credential disclosure through source code, defaults, logs, errors, or serialized
  configuration.
tags: nestjs, configuration, secrets, security
```

Debe establecer:

- no hardcodear secretos reales;
- no proporcionar defaults inseguros;
- permitir variables de entorno y gestores externos;
- priorizar la solución existente;
- validar presencia y formato sin revelar valores;
- no serializar namespaces ni `process.env` completos;
- no incluir tokens, passwords, keys o credenciales en excepciones;
- sanitizar antes de loguear;
- permitir nombre de variable, path, tipo esperado y restricción incumplida.

Ejemplo correcto:

```typescript
if (!config.apiKey) {
  throw new Error('PAYMENTS_API_KEY is required');
}
```

Ejemplo de sanitización:

```typescript
try {
  return paymentsSchema.parse(candidate);
} catch {
  throw new Error('Invalid payments configuration: PAYMENTS_API_KEY is missing or malformed');
}
```

## 9. Propietarios normativos

| Tema                                              | Tarjeta propietaria                                     |
| ------------------------------------------------- | ------------------------------------------------------- |
| Ruta y ownership                                  | `config-locate-configuration-by-ownership`              |
| Namespace, defaults, overrides y validación final | `config-build-and-validate-namespaced-configuration`    |
| Carga por root module o contexto                  | `config-register-configuration-per-application-context` |
| Consumo tipado e inmutable                        | `config-inject-namespaced-configuration`                |
| Acceso a `process.env` y proveedores externos     | `config-isolate-external-configuration-sources`         |
| Contrato de `forRoot` y `forRootAsync`            | `config-validate-dynamic-module-options`                |
| Confidencialidad de secretos y errores            | `config-avoid-hardcoded-secrets`                        |
| Testing                                           | Fuera de las tarjetas `config-`                         |

## 10. Actualización de enlaces

Buscar y actualizar todas las apariciones de:

```text
config-place-files-under-src-config
config-use-namespaced-register-as-factories
config-validate-environment-with-zod
config-register-configuration-in-app-module
config-prevent-direct-environment-access
```

Revisar como mínimo:

- `SKILL.md`;
- `README.md`;
- todas las tarjetas de `references/`;
- documentos compilados o índices;
- evaluaciones de la skill;
- documentación que liste tarjetas por nombre.

No dejar aliases normativos ni copias duplicadas. La trazabilidad de renombres debe vivir en README
o en este plan.

## 11. Fuentes técnicas

Antes de cerrar ejemplos y afirmaciones no triviales, verificar documentación oficial vigente de:

- NestJS Configuration;
- custom configuration files;
- namespaced configuration;
- `registerAs`;
- `ConfigType`;
- partial registration;
- dynamic modules;
- `forRootAsync`;
- custom providers;
- versión de Zod utilizada.

Cada tarjeta debe incluir al menos una referencia HTTPS oficial. No usar blogs como fuente primaria
si existe documentación oficial.

## 12. Evaluación mediante `skill-creator`

La actualización no se considera terminada solo porque Markdown y frontmatter sean válidos.

Después de escribir, seguir el proceso vigente de `skill-creator` para evaluar una skill modificada.

Casos mínimos de comportamiento:

1. Recomendar ubicación basada en ownership, no imponer `src/config`.
2. Construir un namespace completo con defaults y overrides explícitos.
3. Validar el objeto final una sola vez.
4. No obligar Zod cuando el proyecto tiene un validador equivalente.
5. Usar Zod en ejemplos nuevos.
6. No exigir `env.validation.ts`.
7. Registrar namespaces por application context.
8. Inyectar configuración tipada sin strings dispersos.
9. Evitar `process.env` en consumidores.
10. Validar opciones de módulos dinámicos.
11. No exponer secretos en logs o errores.
12. No introducir reglas de testing.

Casos mínimos de triggering:

- “Organiza la configuración de una aplicación NestJS.”
- “Revisa cómo usamos `@nestjs/config`.”
- “Crea un namespace tipado para pagos.”
- “Configura un worker y una API con namespaces distintos.”
- “Valida las opciones de un módulo dinámico NestJS.”
- “Evita que los servicios lean directamente `process.env`.”

Cuando `skill-creator` lo requiera, comparar resultados con y sin la skill. Las assertions deben
evaluar decisiones observables, no coincidencias textuales.

## 13. Validación técnica y documental

Validación estructural:

```bash
python scripts/quick_validate.py skills/typescript/nestjs-practices
```

Si la interfaz real difiere, usar la forma indicada por la ayuda del script o por `skill-creator`.

Validación completa:

```bash
pnpm validate
```

Verificaciones adicionales:

1. No existen referencias a archivos eliminados.
2. Todos los enlaces relativos resuelven.
3. Cada tarjeta cumple el template.
4. `SKILL.md` es conciso.
5. README no contiene normativa task-time.
6. No existe tarjeta de testing.
7. La tarjeta consolidada usa exactamente:

   ```yaml
   tags: nestjs, configuration, validation, register-as
   ```

8. Ningún ejemplo imprime o interpola secretos.
9. Ningún ejemplo correcto obliga una ruta universal.
10. El diff completo fue inspeccionado.

Búsquedas sugeridas:

```bash
rg "config-place-files-under-src-config|config-use-namespaced-register-as-factories|config-validate-environment-with-zod|config-register-configuration-in-app-module|config-prevent-direct-environment-access"
```

```bash
rg "process\.env" skills/typescript/nestjs-practices/references/config-*.md
```

La segunda búsqueda puede devolver resultados válidos en boundaries. Revisar que no aparezca en
consumidores correctos.

```bash
rg "apiKey|password|secret|token" skills/typescript/nestjs-practices/references/config-*.md
```

Revisar manualmente que no haya exposición de valores.

## 14. Orden de edición recomendado

1. Leer `skill-creator` y todos los archivos actuales.
2. Crear `config-build-and-validate-namespaced-configuration.md`.
3. Crear `config-validate-dynamic-module-options.md`.
4. Reescribir o renombrar las otras cinco tarjetas objetivo.
5. Añadir enlaces relativos.
6. Actualizar `SKILL.md`.
7. Actualizar `README.md`.
8. Buscar nombres antiguos.
9. Eliminar tarjetas reemplazadas.
10. Ejecutar validación estructural.
11. Ejecutar evals con `skill-creator`.
12. Ejecutar `pnpm validate`.
13. Inspeccionar diff.
14. Corregir problemas demostrados.
15. No hacer commit ni push sin solicitud explícita.

## 15. Estrategia de commits, si se solicita

El repositorio prohíbe commits automáticos sin solicitud explícita.

Commit único sugerido:

```text
refactor(nestjs-practices): consolidate config guidance
```

Si se autorizan varios commits:

1. Reestructuración de tarjetas `config-`.
2. Navegación e inventario.
3. Evals y ajustes derivados de validación.

No separar eliminación y reemplazo si se dejan enlaces rotos.

## 16. Criterios de aceptación

- [ ] Se cargó y siguió `skill-creator`.
- [ ] Se respetó `AGENTS.md`.
- [ ] El catálogo final contiene las siete tarjetas objetivo.
- [ ] Construcción y validación tienen un único propietario.
- [ ] La validación global es opcional y no duplica restricciones.
- [ ] La ubicación depende de ownership y convenciones.
- [ ] Los namespaces son semánticos y estables.
- [ ] Defaults, overrides, transformaciones y derivados tienen precedencia explícita.
- [ ] Los contratos son read-only.
- [ ] El registro se expresa por application context.
- [ ] La inyección tipada es el patrón principal.
- [ ] Las fuentes externas están encapsuladas.
- [ ] Los módulos dinámicos validan en su boundary.
- [ ] Los secretos no se hardcodean ni aparecen en diagnósticos.
- [ ] No hay reglas de testing en `config-`.
- [ ] `SKILL.md` solo contiene activación, workflow y navegación.
- [ ] README solo contiene inventario y mantenimiento.
- [ ] No hay enlaces a tarjetas retiradas.
- [ ] Todas las tarjetas cumplen el template.
- [ ] `quick_validate.py` termina correctamente.
- [ ] Las evals de `skill-creator` demuestran mejora y triggering correcto.
- [ ] `pnpm validate` termina correctamente.
- [ ] El diff fue revisado.
- [ ] No se hizo commit ni push sin autorización.

## 17. Riesgos y mitigaciones

| Riesgo                                                  | Mitigación                                                                |
| ------------------------------------------------------- | ------------------------------------------------------------------------- |
| Duplicar validación entre factory y `env.validation.ts` | Dar ownership autoritativo a la factory y limitar el validador global.    |
| Convertir Zod en requisito accidental                   | Normativa agnóstica; Zod solo en ejemplos.                                |
| Sobrecargar la tarjeta consolidada                      | Mantener solo decisiones del boundary de construcción y validación final. |
| Repetir seguridad en varias tarjetas                    | Dejar confidencialidad y sanitización en la tarjeta de secretos.          |
| Romper enlaces                                          | Buscar todas las referencias antes de eliminar nombres antiguos.          |
| Hacer `SKILL.md` demasiado extenso                      | Mantenerlo como mapa y mover detalle a `references/`.                     |
| Incluir testing fuera de alcance                        | Rechazar secciones normativas de unit, integration o E2E.                 |
| Inventar APIs                                           | Verificar documentación oficial y versión.                                |
| Sobrescribir cambios del usuario                        | Volver a leer archivos y revisar diff.                                    |
| Evaluar solo sintaxis                                   | Ejecutar el ciclo de `skill-creator`.                                     |

## 18. Entregables de la implementación

1. Lista de archivos creados, renombrados, modificados y eliminados.
2. Resumen de aplicación de las decisiones.
3. Resultado de `quick_validate.py`.
4. Resultado de evals con `skill-creator`.
5. Resultado de `pnpm validate`.
6. Observaciones sobre enlaces y referencias oficiales.
7. Diff resumido por tarjeta.
8. Declaración de que no se hizo commit ni push, salvo solicitud.

## 19. Resumen operativo

```text
Read AGENTS.md
  → load ~/.agents/skills/skill-creator
  → inspect current skill and all config cards
  → create the consolidated card
  → rename and rewrite remaining cards
  → add dynamic module options
  → update SKILL.md navigation
  → update README inventory
  → remove obsolete cards and links
  → validate structure
  → run skill-creator evaluations
  → run pnpm validate
  → inspect diff
```

El resultado debe ser un catálogo `config-` compacto, cohesivo y navegable, en el que cada decisión
tenga un propietario normativo claro y `SKILL.md` cargue únicamente el detalle necesario para la
tarea en curso.
