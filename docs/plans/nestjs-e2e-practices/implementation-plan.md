# Plan de implementación de la skill `nestjs-e2e-practices`

Este plan define la creación de una skill independiente para diseñar, implementar, revisar y
corregir pruebas E2E reales en aplicaciones NestJS. La skill debe comprobar el sistema ejecutable
desde HTTP hasta la persistencia, controlar el orden mediante dos niveles de orquestación y permitir
dobles únicamente en adaptadores de servicios externos explícitamente delimitados.

> Estado: implementación finalizada y aceptación formal confirmada; triggering validado y optimizado
> en OpenCode.

## Ruta rápida

1. Extraer de `nestjs-practices` las reglas E2E existentes y asignarlas a la nueva skill como único
   propietario normativo.
2. Crear un `SKILL.md` breve que active la skill, inspeccione el proyecto y dirija al agente hacia
   las tarjetas pertinentes.
3. Crear cuatro tarjetas detalladas que agrupen reglas con el mismo contexto de aplicación.
4. Añadir README, registro público, marketplace y evaluaciones comparativas.
5. Validar estructura, triggering y calidad de los resultados antes de aceptar la implementación.

## 1. Resultado esperado

Al terminar, el repositorio dispondrá de `skills/typescript/nestjs-e2e-practices/` como fuente
canónica para E2E de NestJS. La skill deberá permitir que un agente:

- Descubra el bootstrap, módulos, adaptador HTTP, validación, autenticación, persistencia, runner y
  comandos reales del proyecto antes de escribir pruebas.
- Ejecute la implementación real mediante endpoints HTTP públicos.
- Use el mismo módulo raíz y las decisiones de bootstrap relevantes de producción.
- Trabaje contra una base de datos real, temporal, aislada y migrada.
- Cree datos por HTTP y reserve seeds reales para precondiciones sin endpoint público.
- Obtenga credenciales y tokens por flujos reales de autenticación.
- Organice la ejecución mediante un orquestador principal y orquestadores por funcionalidad.
- Registre suites de endpoint de forma explícita y determinista, sin depender del orden del runner.
- Reutilice contratos válidos canónicos y derive variantes inválidas sin contaminar fixtures.
- Valide status, contrato público, errores, cabeceras, efectos posteriores y ausencia de secretos.
- Mantenga reales controladores, guards, pipes, interceptores, servicios internos, repositorios,
  Prisma u otro ORM y la base de datos.
- Sustituya únicamente adaptadores externos fuera del proceso cuando ejecutarlos sea inseguro,
  destructivo, costoso, no determinista o no disponible; el envío real de correo es el caso de
  referencia.
- Informe qué recorrido fue real, qué frontera externa se sustituyó y cómo se verificó la suite.

## 2. Alcance

### Incluido

- Nueva skill `nestjs-e2e-practices` dentro de la categoría `typescript`.
- `SKILL.md` con frontmatter, disparadores, flujo de trabajo, mapa de tarjetas y contrato de salida.
- Cuatro tarjetas detalladas bajo `references/`.
- README de inventario y mantenimiento.
- Migración de la propiedad normativa desde las seis tarjetas E2E actuales de `nestjs-practices`.
- Registro de la skill en README raíz y marketplace.
- Evals de comportamiento y triggering siguiendo `skill-creator`.
- Validación estructural, documental y de enlaces.

### Fuera de alcance

- Implementar E2E en una aplicación consumidora concreta.
- Proveer una librería reusable de testing o un paquete npm.
- Obligar a usar Fastify, Prisma, Zod, Jest o Supertest cuando el proyecto use otras alternativas.
- Mockear servicios internos por comodidad.
- Probar la disponibilidad real, entregabilidad o reputación de un proveedor externo de correo.
- Convertir pruebas E2E en sustituto de pruebas unitarias, de integración o de persistencia.
- Definir una arquitectura universal para aplicaciones NestJS fuera del contexto E2E.

## 3. Decisiones de diseño

### D1. Crear una skill independiente

`nestjs-practices` tiene un catálogo amplio de arquitectura y runtime. E2E ya exige reglas de
infraestructura, lifecycle, datos, contratos y evaluación suficientes para justificar una skill
especializada. Mantenerlas separadas mejora el triggering y evita cargar decisiones E2E durante
tareas NestJS no relacionadas con pruebas.

La separación debe tener propietario único: las tarjetas E2E actuales se eliminan de
`nestjs-practices` después de migrar su contenido válido. No se mantendrán copias normativas en dos
skills.

### D2. Mantener `SKILL.md` como mapa operativo

`SKILL.md` contendrá únicamente:

- Capacidad y disparadores en `description`.
- Condiciones de aplicación y límites.
- Inspección inicial obligatoria del proyecto consumidor.
- Mapa para seleccionar tarjetas.
- Flujo de ejecución y verificación.
- Contrato de salida.

Las reglas, razones, excepciones, ejemplos y fuentes vivirán en `references/`.

### D3. Agrupar reglas que comparten contexto

La atomicidad no significa un archivo por frase. Una tarjeta puede contener variantes que comparten
alcance, impacto y criterios de aplicación. Se proponen cuatro tarjetas:

| Tarjeta                                          | Contexto coherente que posee                                                 |
| ------------------------------------------------ | ---------------------------------------------------------------------------- |
| `e2e-orchestrate-execution-and-lifecycle.md`     | Orden, dos niveles de orquestación, discovery, contexto y teardown           |
| `e2e-run-real-application-and-infrastructure.md` | Bootstrap productivo, HTTP real, base aislada, migraciones, providers y auth |
| `e2e-build-data-and-assert-contracts.md`         | Fixtures, seeds, payloads, contratos, seguridad y efectos observables        |
| `e2e-isolate-external-service-boundaries.md`     | Criterios, ubicación y reporte de dobles para dependencias externas          |

Se separará una regla en otra tarjeta solo si puede activarse, fallar y evaluarse de manera
independiente del resto de su contexto.

### D4. Usar dos niveles explícitos de orquestación

La skill exigirá:

1. Un orquestador principal descubierto por el runner.
2. Un orquestador por funcionalidad importado y registrado por el principal.
3. Suites de endpoint registradas por su orquestador de funcionalidad.

El orden debe surgir de llamadas de registro explícitas dentro de un único árbol de ejecución, no de
orden alfabético, `runInBand`, secuenciadores implícitos ni orden de archivos descubierto por Jest.

La orquestación requiere además un proyecto E2E explícito del runner. Para Jest, `testMatch` o
`testRegex` debe descubrir únicamente el orquestador principal; las suites importadas deben usar un
sufijo o directorio que no coincida con el patrón. `maxWorkers: 1` o `--runInBand` puede proteger
una infraestructura compartida, pero no reemplaza el control de discovery ni constituye el mecanismo
de orden. La configuración debe evitar `test.concurrent` en flujos que comparten contexto mutable.

El proceso que ejecuta el orquestador principal debe crear y cerrar NestJS. `globalSetup` puede
preparar recursos externos, pero no debe crear una instancia de aplicación que las suites intenten
reutilizar: Jest no expone las variables de `globalSetup` a los entornos de prueba.
`setupFilesAfterEnv` debe reservarse para matchers, hooks de higiene y configuración que no posea la
aplicación.

### D5. Definir propietarios inequívocos del lifecycle

| Recurso                                                             | Propietario                                 |
| ------------------------------------------------------------------- | ------------------------------------------- |
| Entorno E2E, base temporal, migraciones, aplicación y cierre global | Orquestador principal                       |
| Contexto y recursos de una funcionalidad                            | Orquestador de funcionalidad                |
| Datos exclusivos de un caso                                         | Caso o suite de endpoint que los crea       |
| Adaptador externo sustituido                                        | Harness principal, con override documentado |

El orquestador principal debe restaurar variables de entorno y eliminar recursos incluso cuando
fallen setup, pruebas o cleanup. Los orquestadores de funcionalidad nunca cierran la aplicación ni
eliminan la base global.

### D6. Priorizar datos creados por HTTP

Los fixtures deben crearse mediante endpoints disponibles para que el flujo compruebe validación,
servicios y persistencia. Un seed mediante el ORM real es válido solo cuando la precondición no
pueda obtenerse por HTTP, por ejemplo un estado administrativo no expuesto. El plan no permitirá SQL
directo para evitar invariantes.

### D7. Delimitar la excepción de servicios externos

La excepción no autoriza mockear el servicio de aplicación que coordina el envío. Se sustituye el
adaptador que cruza el límite del proceso, por ejemplo `EmailProvider` o `MailTransport`, mientras
permanecen reales:

- Endpoint y controlador.
- Validación y autorización.
- Servicio de aplicación.
- Renderizado o construcción del mensaje si pertenece a la aplicación.
- Persistencia, eventos y actualización de estado local.

El doble debe capturar el contrato saliente para afirmar destinatario, plantilla y datos públicos,
sin efectuar una entrega real.

### D8. Ser agnóstica a tecnologías reemplazables

Fastify, Zod, Prisma, Jest y Supertest pueden aparecer en ejemplos claramente ilustrativos porque
son frecuentes en NestJS, pero la norma será replicar las decisiones del proyecto. La skill debe
descubrir y conservar adaptador, ORM, validador, runner, cliente HTTP y gestor de paquetes reales.

### D9. Evaluar la skill antes de considerarla terminada

La creación seguirá el ciclo de `skill-creator`: draft, evals con y sin skill, assertions objetivas,
benchmark, revisión humana e iteración. La validación sintáctica por sí sola no demuestra que la
skill cambie correctamente el comportamiento del agente.

## 4. Árbol de archivos objetivo

```text
skills/
└── typescript/
    ├── nestjs-e2e-practices/
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── references/
    │   │   ├── e2e-orchestrate-execution-and-lifecycle.md
    │   │   ├── e2e-run-real-application-and-infrastructure.md
    │   │   ├── e2e-build-data-and-assert-contracts.md
    │   │   └── e2e-isolate-external-service-boundaries.md
    │   └── evals/
    │       └── evals.json
    └── nestjs-practices/
        ├── SKILL.md
        ├── README.md
        └── references/
            └── ... # Sin las seis tarjetas test-e2e-* migradas.

docs/
└── plans/
    └── nestjs-e2e-practices/
        └── implementation-plan.md

.claude-plugin/
└── marketplace.json

README.md
```

El workspace generado por `skill-creator` para comparar iteraciones será temporal o ignorado y no
formará parte de la distribución salvo que la convención del repositorio cambie explícitamente.

## 5. Inventario de cambios

### Archivos a crear

| Archivo                                                                                            | Propósito                                                   |
| -------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| `skills/typescript/nestjs-e2e-practices/SKILL.md`                                                  | Activación, navegación, workflow y salida de la nueva skill |
| `skills/typescript/nestjs-e2e-practices/README.md`                                                 | Inventario humano y mantenimiento                           |
| `skills/typescript/nestjs-e2e-practices/references/e2e-orchestrate-execution-and-lifecycle.md`     | Orquestación principal/funcional y lifecycle                |
| `skills/typescript/nestjs-e2e-practices/references/e2e-run-real-application-and-infrastructure.md` | Aplicación e infraestructura reales                         |
| `skills/typescript/nestjs-e2e-practices/references/e2e-build-data-and-assert-contracts.md`         | Datos, payloads y contratos públicos                        |
| `skills/typescript/nestjs-e2e-practices/references/e2e-isolate-external-service-boundaries.md`     | Excepción controlada para servicios externos                |
| `skills/typescript/nestjs-e2e-practices/evals/evals.json`                                          | Prompts y assertions de comportamiento                      |

### Archivos a modificar

| Archivo                                        | Cambio                                                                                      |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `skills/typescript/nestjs-practices/SKILL.md`  | Retirar alcance, navegación y contrato E2E; mantener prácticas NestJS generales             |
| `skills/typescript/nestjs-practices/README.md` | Retirar inventario E2E y registrar la separación de responsabilidad si aporta mantenimiento |
| `.claude-plugin/marketplace.json`              | Registrar `./skills/typescript/nestjs-e2e-practices` en el plugin TypeScript                |
| `README.md`                                    | Añadir la skill a la tabla pública con un disparador conciso                                |

### Archivos a eliminar después de migrar su contenido

```text
skills/typescript/nestjs-practices/references/test-e2e-replicate-production-bootstrap.md
skills/typescript/nestjs-practices/references/test-e2e-use-real-dependencies.md
skills/typescript/nestjs-practices/references/test-e2e-own-shared-context-lifecycle.md
skills/typescript/nestjs-practices/references/test-e2e-organize-suites-by-size.md
skills/typescript/nestjs-practices/references/test-e2e-derive-invalid-payloads.md
skills/typescript/nestjs-practices/references/test-e2e-assert-public-contracts.md
```

La eliminación ocurrirá en la misma unidad de trabajo que crea las tarjetas reemplazantes y
actualiza la navegación, para que el repositorio nunca quede con reglas inaccesibles o duplicadas.

## 6. Diseño de `SKILL.md`

### Frontmatter propuesto

```yaml
---
name: nestjs-e2e-practices
description: >
  Design, implement, review, and repair real HTTP end-to-end tests for NestJS applications. Use when
  working on NestJS E2E suites, production-like test bootstrap, main or feature orchestrators,
  deterministic test order, isolated real databases, migrations, HTTP-created fixtures, real
  authentication, public API contracts, teardown, or controlled doubles for external services such
  as email providers. Do not use for unit tests, non-NestJS E2E tests, or browser-only UI testing.
license: MIT
metadata:
  author: AutanaSoft
  version: '0.1.0'
---
```

La descripción final deberá validarse mediante evals de triggering. No se debe optimizar solo por
palabras clave: debe distinguir E2E de NestJS de unit tests, integración de repositorios y
Playwright de frontend.

### Secciones previstas

1. `# NestJS E2E Practices`
2. `## When to Apply`
3. `## Hard Rules`
4. `## Workflow`
5. `## Decision Map`
6. `## Verification`
7. `## Output Contract`

### Workflow previsto

1. Identificar el alcance solicitado: creación, revisión, corrección o migración E2E.
2. Inspeccionar bootstrap productivo, módulo raíz, adaptador, pipes, filtros, interceptores,
   prefijo, logging y request ID.
3. Inspeccionar persistencia, migraciones, entorno E2E, autenticación y dependencias externas.
4. Inspeccionar discovery, concurrencia y comandos del runner.
5. Cargar solo las tarjetas que correspondan a las decisiones presentes.
6. Diseñar o ajustar el árbol de orquestación antes de escribir casos.
7. Implementar flujos HTTP y cleanup con recursos reales.
8. Ejecutar la unidad enfocada y luego el orquestador principal completo.
9. Reportar el contrato de salida.

### Mapa de decisión previsto

| Si la tarea involucra                                             | Leer                                                        |
| ----------------------------------------------------------------- | ----------------------------------------------------------- |
| Orden, discovery, orquestadores, contexto, cleanup o cierre       | `references/e2e-orchestrate-execution-and-lifecycle.md`     |
| Bootstrap, base temporal, migraciones, providers o autenticación  | `references/e2e-run-real-application-and-infrastructure.md` |
| Fixtures, seeds, payloads, errores, contratos o campos sensibles  | `references/e2e-build-data-and-assert-contracts.md`         |
| Correo, pagos, SMS, webhooks u otra dependencia fuera del proceso | `references/e2e-isolate-external-service-boundaries.md`     |

### Contrato de salida previsto

La skill debe pedir al agente que reporte:

- Archivos creados o modificados.
- Orquestador principal, orquestadores de funcionalidad y orden registrado.
- Flujos HTTP y componentes internos reales ejercitados.
- Estrategia de base aislada, migraciones y teardown.
- Datos creados por HTTP y seeds justificados.
- Constantes o fábricas válidas reutilizadas y variantes inválidas derivadas.
- Contratos, cabeceras, efectos y campos sensibles verificados.
- Adaptadores externos sustituidos, justificación y recorrido real conservado.
- Comandos ejecutados y resultado de la suite enfocada y completa.
- Riesgos o verificaciones no ejecutadas.

## 7. Diseño detallado de tarjetas

Todas las tarjetas deberán seguir `docs/skill-authoring/reference-card-template.md`: `title` y H2
idénticos, impacto permitido, `impactDescription`, máximo cuatro tags, ejemplos incorrecto/correcto
comparables, bloques con lenguaje y al menos una fuente HTTPS oficial.

### 7.1 `e2e-orchestrate-execution-and-lifecycle.md`

**Título propuesto:** `Orchestrate E2E execution and lifecycle explicitly`

**Impacto:** `CRITICAL`.

**Tags:** `nestjs`, `e2e`, `orchestration`, `lifecycle`.

**Reglas coherentes de la tarjeta:**

- El runner descubre un único orquestador principal para la ejecución completa.
- El principal registra orquestadores de funcionalidad en el orden requerido.
- Cada orquestador de funcionalidad registra suites por endpoint.
- Las suites importadas usan nombres o ubicaciones excluidos del discovery directo.
- Un proyecto Jest E2E define `testMatch` o `testRegex` para descubrir solo el principal.
- `maxWorkers: 1` o `--runInBand` es una defensa para recursos compartidos, no una garantía de
  orden.
- Los flujos orquestados no usan `test.concurrent` ni dependen de un `testSequencer` personalizado.
- `globalSetup` no crea la aplicación NestJS que necesitan las suites.
- `setupFilesAfterEnv` se limita a matchers y restauración de estado global.
- El principal posee entorno, base, aplicación y teardown global.
- Cada funcionalidad posee su contexto tipado y limpieza local.
- Cada prueba crea sus datos salvo dependencia de flujo declarada.
- El cleanup ocurre en orden inverso y dentro de `finally`.

**Por qué viven juntas:** orden, registro, contexto y teardown forman un único árbol de ownership.
Si se separan sin coordinación, aparecen doble ejecución, cierres prematuros y estado dependiente
del orden.

**Ejemplo incorrecto previsto:** varios `*.e2e-spec.ts` descubiertos independientemente comparten un
singleton y esperan orden alfabético; uno ejecuta `app.close()` en su `afterAll`.

**Ejemplo correcto previsto:** un `main.e2e-spec.ts` registra `authE2E`, `usersE2E` y `settingsE2E`
como funciones; cada función registra suites de endpoint y recibe contextos mediante getters.

La tarjeta incluirá además una configuración Jest recomendada y adaptable al proyecto:

```typescript
import type { Config } from 'jest';

const config: Config = {
  displayName: 'e2e',
  testEnvironment: 'node',
  testMatch: ['<rootDir>/test/main.e2e-spec.ts'],
  maxWorkers: 1,
  detectOpenHandles: true,
  forceExit: false,
};

export default config;
```

`transform`, aliases, extensiones y `rootDir` deben derivarse de la configuración real del proyecto.
No se recomendará `forceExit: true`, porque puede ocultar handles filtrados. `detectOpenHandles` es
una ayuda diagnóstica y puede reservarse para CI o troubleshooting si su costo resulta
significativo.

```typescript
describe('API E2E', () => {
  let environment: E2EEnvironment;

  beforeAll(async () => {
    environment = await createE2EEnvironment();
  });

  registerAuthE2E(() => environment);
  registerUsersE2E(() => environment);
  registerSettingsE2E(() => environment);

  afterAll(async () => {
    await environment.dispose();
  });
});
```

El ejemplo completo debe explicar que la secuencia de llamadas registra el orden dentro del mismo
árbol Jest, pero no convierte casos arbitrarios en una cadena frágil. Los datos compartidos
requieren una dependencia de flujo explícita.

La tarjeta explicará que Jest ejecuta serialmente los tests encontrados dentro de un mismo archivo
salvo uso explícito de APIs concurrentes. Un `testSequencer` ordena archivos descubiertos, pero no
corrige una arquitectura que descubre varios entry points con ownership compartido.

**Fuentes a verificar:** configuración, discovery, orden, CLI, `globalSetup`, `globalTeardown` y
setup/teardown oficiales de Jest 30 o la versión usada; lifecycle de NestJS y Fastify cuando
aparezcan en el ejemplo.

### 7.2 `e2e-run-real-application-and-infrastructure.md`

**Título propuesto:** `Run the real application and isolated infrastructure`

**Impacto:** `CRITICAL`.

**Tags:** `nestjs`, `e2e`, `database`, `bootstrap`.

**Reglas coherentes de la tarjeta:**

- Arrancar el mismo módulo raíz y configurador de bootstrap que producción.
- Replicar adaptador, pipes, filtros, interceptores, prefijo, serialización, logging y request ID
  cuando existan.
- Usar una base temporal exclusiva con nombre impredecible y credenciales E2E dedicadas.
- Aplicar migraciones reales antes de iniciar NestJS.
- Resolver providers reales del contenedor.
- Ejecutar endpoints HTTP públicos, incluida autenticación real.
- Cerrar NestJS, ORM, pools, transports y base temporal de forma determinista.
- Rechazar URLs compartidas o de producción antes de crear o eliminar recursos.

**Por qué viven juntas:** bootstrap, persistencia y providers constituyen el runtime que la prueba
afirma representar. Separarlos permitiría una aplicación real conectada a infraestructura falsa o
una base real detrás de módulos sustituidos.

**Ejemplo incorrecto previsto:** `TestingModule` con solo `UsersModule`, SQLite en memoria,
repositorio mockeado y token preemitido.

**Ejemplo correcto previsto:** `createE2EEnvironment()` valida `DATABASE_URL_ADMIN_E2E`, crea una
base, aplica migraciones, configura la URL temporal y arranca `AppModule` mediante el bootstrap
compartido.

```typescript
export async function createE2EEnvironment(): Promise<E2EEnvironment> {
  const database = await temporaryDatabase.create();

  try {
    await migrations.apply(database.url);
    const app = await createApplication({ databaseUrl: database.url });
    await app.init();

    return createEnvironmentHandle(app, database);
  } catch (error: unknown) {
    await database.drop();
    throw error;
  }
}
```

El ejemplo no debe presentar `temporaryDatabase` como magia: la tarjeta describirá su contrato,
validaciones destructivas y cleanup esperado, dejando la implementación al stack real del proyecto.

**Fuentes a verificar:** testing de NestJS, lifecycle del adaptador, migraciones del ORM usado en el
ejemplo y documentación oficial de PostgreSQL sobre creación/eliminación de bases cuando aplique.

### 7.3 `e2e-build-data-and-assert-contracts.md`

**Título propuesto:** `Build realistic E2E data and assert public contracts`

**Impacto:** `HIGH`.

**Tags:** `nestjs`, `e2e`, `fixtures`, `api-contract`.

**Reglas coherentes de la tarjeta:**

- Crear fixtures mediante endpoints públicos cuando estén disponibles.
- Usar seeds reales solo para estados no creables por HTTP y documentar el motivo.
- Mantener constantes o fábricas válidas como contrato base.
- Generar identidades únicas por caso o flujo.
- Derivar payloads inválidos mediante copia local y cambiar solo el campo bajo prueba.
- Copiar ramas anidadas modificadas; nunca mutar fixtures compartidos.
- Cubrir éxito, validación, autorización, ausencia, conflicto y límites aplicables.
- Afirmar status, schema/estructura pública, cabeceras relevantes y efecto posterior.
- Afirmar ausencia de passwords, hashes, secretos, metadata interna y tokens no contractuales.
- Evitar snapshots opacos y full-body equality sobre valores volátiles.

**Por qué viven juntas:** la calidad de una assertion depende del dato y del escenario que la
produce. Fixtures, variantes inválidas y contrato observable forman la unidad de diseño de un caso
E2E por endpoint.

**Ejemplo incorrecto previsto:** objeto global mutado, inserción directa pese a existir
`POST /users`, solo `.expect(201)` y snapshot completo.

**Ejemplo correcto previsto:** fábrica válida con identidad única, creación HTTP y una variante
inválida local.

```typescript
const validPayload = createValidUserPayload();
const created = await api.post('/users').send(validPayload).expect(201);

expect(created.body).toEqual(
  expect.objectContaining({
    id: expect.any(String),
    email: validPayload.email,
  }),
);
expect(created.body).not.toHaveProperty('password');
expect(created.body).not.toHaveProperty('passwordHash');

const invalidPayload = { ...createValidUserPayload(), email: 'invalid-email' };
const invalid = await api.post('/users').send(invalidPayload).expect(400);
expect(invalid.body).toEqual(expect.objectContaining({ error: expect.anything() }));
```

**Fuentes a verificar:** testing y serialización de NestJS, matcher o schema usado, y semántica de
copia superficial de JavaScript/TypeScript.

### 7.4 `e2e-isolate-external-service-boundaries.md`

**Título propuesto:** `Isolate only external service boundaries in E2E tests`

**Impacto:** `CRITICAL`.

**Tags:** `nestjs`, `e2e`, `external-service`, `test-double`.

**Reglas coherentes de la tarjeta:**

- No sustituir servicios propios, repositorios, guards, auth, ORM ni base de datos.
- Preferir un entorno real de sandbox cuando sea seguro y determinista.
- Permitir un doble solo para una dependencia fuera del proceso que sea no determinista,
  destructiva, costosa o indisponible.
- Sustituir el adaptador de borde mediante DI, no aplicar `spyOn` al servicio de aplicación.
- Mantener real el recorrido interno hasta el puerto externo.
- Afirmar el contrato saliente capturado por el doble.
- Restablecer overrides y estado entre ejecuciones.
- Reportar frontera, motivo, cobertura conservada y limitación residual.

**Por qué viven juntas:** los criterios de admisión, ubicación del doble y evidencia requerida
forman una sola política de frontera. Separarlos facilitaría aceptar mocks sin preservar el flujo
real.

**Ejemplo incorrecto previsto:** mock de `RequestPasswordResetService.execute()` que devuelve éxito,
por lo cual no se comprueban persistencia, token ni construcción del correo.

**Ejemplo correcto previsto:** override de `MAIL_TRANSPORT` con un adaptador capturador; el
endpoint, servicio, token, plantilla y persistencia siguen siendo reales.

```typescript
const mailTransport = new CapturingMailTransport();
const app = await createApplication({
  externalOverrides: [{ token: MAIL_TRANSPORT, useValue: mailTransport }],
});

await request(app.getHttpServer())
  .post('/auth/forgot-password')
  .send({ email: user.email })
  .expect(204);

expect(mailTransport.messages).toContainEqual(
  expect.objectContaining({
    to: user.email,
    template: 'reset-password',
  }),
);
```

La tarjeta aclarará que esta prueba no demuestra entregabilidad del proveedor. Esa garantía requiere
pruebas contractuales o de integración separadas contra el sandbox del proveedor.

**Fuentes a verificar:** custom providers y testing modules de NestJS, más documentación oficial del
proveedor elegido si se incluye un ejemplo específico.

## 8. Estructura E2E que la skill debe recomendar

La estructura concreta se adapta al proyecto, pero el modelo de referencia será:

```text
test/
├── main.e2e-spec.ts                         # Único entry point descubierto para ejecución total
├── support/
│   ├── e2e-environment.ts                  # Base temporal, migraciones y variables de entorno
│   ├── real-e2e-application.ts             # Bootstrap derivado de producción
│   ├── external-boundary-overrides.ts      # Overrides externos explícitos
│   └── e2e-assertions.ts                   # Helpers contractuales sin ocultar intención
├── fixtures/
│   ├── auth.fixture.ts
│   └── users.fixture.ts
└── modules/
    ├── auth/
    │   ├── auth.e2e-orchestrator.ts
    │   ├── auth.e2e-context.ts
    │   └── suites/
    │       ├── sign-up.e2e-suite.ts
    │       ├── sign-in.e2e-suite.ts
    │       └── reset-password.e2e-suite.ts
    ├── users/
    │   ├── users.e2e-orchestrator.ts
    │   ├── users.e2e-context.ts
    │   └── suites/
    │       ├── create-user.e2e-suite.ts
    │       ├── list-users.e2e-suite.ts
    │       └── update-user.e2e-suite.ts
    └── health/
        ├── health.e2e-orchestrator.ts
        └── suites/
            ├── live-health.e2e-suite.ts
            └── ready-health.e2e-suite.ts

jest.config.e2e.ts                           # Jest descubre solo main.e2e-spec.ts
```

`*.e2e-suite.ts` es un nombre ilustrativo destinado a evitar discovery directo. La skill deberá
inspeccionar `testMatch`, `testRegex`, roots e ignore patterns antes de elegirlo.

### Ejemplo de composición por funcionalidad

```typescript
export function registerUsersE2E(getEnvironment: () => E2EEnvironment): void {
  describe('Users E2E', () => {
    let context: UsersE2EContext;

    beforeAll(async () => {
      context = await createUsersContext(getEnvironment());
    });

    registerCreateUserSuite(() => context);
    registerListUsersSuite(() => context);
    registerUpdateUserSuite(() => context);

    afterAll(async () => {
      await context.cleanup();
    });
  });
}
```

El principal controla el orden entre funcionalidades. El orquestador de funcionalidad controla el
orden y el contexto dentro de su alcance. Las suites de endpoint no adquieren ni cierran la
aplicación global.

## 9. Fases de implementación

### Fase 0. Proteger línea base

1. Registrar `git status`, diff y archivos no relacionados.
2. Ejecutar `python scripts/quick_validate.py skills/typescript/nestjs-practices`.
3. Ejecutar `pnpm validate` y guardar el resultado de referencia.
4. Crear snapshot de `nestjs-practices` para comparar triggering y outputs.
5. Inventariar las seis tarjetas E2E actuales y mapear contenido que debe conservarse.

**Criterio de salida:** baseline reproducible, cambios ajenos identificados y reglas existentes
trazadas antes de eliminarlas.

### Fase 1. Crear el esqueleto y triggering

1. Crear el directorio `skills/typescript/nestjs-e2e-practices/`.
2. Crear `SKILL.md` con nombre coincidente y campos permitidos.
3. Redactar descripción inicial con casos positivos y límites negativos.
4. Crear mapa de decisión para las cuatro tarjetas.
5. Definir workflow y contrato de salida sin duplicar reglas.

**Criterio de salida:** entry point válido, menor de 500 líneas y navegable, con capacidad y
disparadores concretos.

### Fase 2. Crear tarjetas detalladas

1. Crear las cuatro tarjetas desde el template local.
2. Migrar las decisiones útiles de las seis tarjetas actuales.
3. Incorporar el orquestador principal y la base temporal aislada como reglas nuevas.
4. Incorporar la configuración Jest E2E: discovery exclusivo, workers defensivos y límites de setup.
5. Incorporar la excepción explícita del adaptador externo de correo.
6. Escribir ejemplos incorrecto/correcto comparables.
7. Verificar APIs y comportamientos contra documentación oficial actual.
8. Enlazar tarjetas relacionadas sin copiar reglas.

**Criterio de salida:** cada regla tiene un único propietario, ejemplos ejecutables en intención y
fuentes oficiales verificadas.

### Fase 3. Completar inventario y migración

1. Crear README de la nueva skill.
2. Retirar E2E de descripción, workflow, mapa y output de `nestjs-practices`.
3. Eliminar las seis tarjetas antiguas tras confirmar su reemplazo.
4. Actualizar README de `nestjs-practices`.
5. Añadir la skill al README raíz.
6. Añadir la ruta al plugin TypeScript en marketplace.

**Criterio de salida:** no existe duplicación normativa; ambas skills son instalables y sus
disparadores se distinguen.

### Fase 4. Crear evals de comportamiento

1. Crear de tres a cinco prompts realistas en `evals/evals.json`.
2. Ejecutar cada prompt con la nueva skill y sin skill en paralelo.
3. Redactar assertions objetivas mientras se ejecutan los casos.
4. Capturar tiempo y tokens de cada ejecución.
5. Calificar resultados, agregar benchmark y analizar fallos no discriminantes.
6. Generar el viewer oficial de `skill-creator` para revisión humana.
7. Iterar solo sobre fallos generalizables.

**Criterio de salida:** la skill mejora de forma observable estructura, realismo, lifecycle,
contratos y tratamiento de dependencias externas.

### Fase 5. Optimizar triggering

1. Crear aproximadamente veinte consultas: positivos y near-misses negativos.
2. Revisarlas con el usuario antes de ejecutar optimización.
3. Medir activación para creación, revisión, corrección y migración E2E NestJS.
4. Medir falsos positivos frente a unit tests, frontend E2E y testing general.
5. Aplicar la mejor descripción solo si mejora el conjunto reservado.

**Criterio de salida:** activación alta en tareas NestJS E2E sin capturar dominios adyacentes.

### Fase 6. Validación final

1. Ejecutar el validador enfocado sobre ambas skills afectadas.
2. Ejecutar `pnpm validate`.
3. Verificar enlaces, frontmatter, inventarios y marketplace.
4. Confirmar la matriz de trazabilidad y criterios de aceptación.
5. Revisar el diff completo y proteger cambios ajenos.
6. Entregar resultados sin commit ni push salvo solicitud explícita.

**Criterio de salida:** validadores verdes, evals revisados y cambio listo para revisión.

## 10. Estrategia de evaluación

### Prompts de comportamiento mínimos

| Caso        | Prompt resumido                                       | Evidencia esperada                                              |
| ----------- | ----------------------------------------------------- | --------------------------------------------------------------- |
| Nueva suite | Crear E2E de auth y users con PostgreSQL real         | Principal, orquestadores funcionales, migraciones y auth HTTP   |
| Revisión    | Auditar varios `*.e2e-spec.ts` dependientes del orden | Detecta discovery independiente y propone composición explícita |
| Correo      | Probar forgot-password sin enviar correos reales      | Sustituye transport externo, no servicio interno                |
| Datos       | Corregir fixtures mutados y assertions débiles        | Fábricas válidas, variantes locales y campos sensibles ausentes |
| Near-miss   | Crear Playwright para una UI sin NestJS               | La skill no debe activarse                                      |

### Assertions objetivas sugeridas

- Define un orquestador principal descubierto por el runner.
- Define un orquestador por funcionalidad y suites por endpoint no descubiertas directamente.
- Registra el orden mediante composición explícita, no por nombres de archivo.
- Configura Jest para descubrir solo el orquestador principal.
- Mantiene las sub-suites fuera de `testMatch`/`testRegex` y evita `test.concurrent`.
- Trata `maxWorkers: 1` o `runInBand` como protección, no como mecanismo de orden.
- No crea la aplicación NestJS en `globalSetup` ni la oculta en `setupFilesAfterEnv`.
- Asigna aplicación, base y teardown global al principal.
- Usa base exclusiva y aplica migraciones reales.
- Reutiliza el módulo raíz y bootstrap productivo.
- Ejecuta endpoints públicos y obtiene tokens mediante auth real.
- Crea datos por HTTP o justifica cada seed.
- No mockea providers internos, repositorios, ORM, guards ni tokens.
- Limita el doble de correo al adaptador externo.
- Asegura el contrato saliente capturado por el doble.
- Deriva payloads inválidos sin mutar fixtures.
- Valida status, estructura, cabeceras, efectos y ausencia de secretos.
- Define cleanup inverso y seguro ante fallos.
- Descubre comandos reales y reporta resultados enfocados y completos.

### Casos de triggering positivos

- "Crea los E2E de un módulo NestJS con Fastify, Prisma y PostgreSQL temporal".
- "Revisa por qué mis specs E2E dependen del orden de Jest".
- "Necesito un orquestador global y uno por módulo para la API NestJS".
- "Prueba el reset de password sin llamar al proveedor real de correo".
- "Asegura que los endpoints no devuelvan passwordHash".

### Near-misses negativos

- Tests unitarios de un servicio NestJS aislado.
- Integración de un repositorio Prisma sin HTTP.
- Playwright/Cypress de una interfaz web que consume una API externa.
- Configuración general de módulos NestJS sin E2E.
- Pruebas contractuales del sandbox de un proveedor de correo.

## 11. Validación

### Comandos

```bash
python scripts/quick_validate.py skills/typescript/nestjs-e2e-practices
python scripts/quick_validate.py skills/typescript/nestjs-practices
pnpm validate
```

### Verificación estructural

- El directorio y `name` son exactamente `nestjs-e2e-practices`.
- `description` declara capacidad y disparadores y no supera 1024 caracteres.
- Solo se usan campos de frontmatter admitidos.
- `SKILL.md` enlaza las cuatro tarjetas y no contiene sus reglas completas.
- README inventaría exactamente las cuatro tarjetas.
- Marketplace y README raíz contienen la nueva skill una sola vez.
- `nestjs-practices` ya no declara propiedad de reglas E2E.
- No quedan enlaces hacia las seis tarjetas eliminadas.

### Verificación de tarjetas

- Título de frontmatter y H2 coinciden exactamente.
- Impacto pertenece al conjunto permitido.
- Hay máximo cuatro tags en kebab-case.
- Cada tarjeta contiene razones, límites y ejemplos comparables.
- Todos los bloques declaran lenguaje.
- Cada tarjeta cita al menos una fuente oficial HTTPS.
- Las reglas con el mismo contexto permanecen agrupadas.
- Las reglas con activación independiente no se duplican entre tarjetas.

### Verificación conceptual

- Existe un orquestador principal además de los funcionales.
- El orden se registra explícitamente en un único árbol de suites.
- Jest descubre únicamente el orquestador principal y no ejecuta sub-suites importadas por separado.
- La configuración no usa `test.concurrent` para flujos compartidos.
- `maxWorkers: 1` es defensivo y no sustituye el patrón de discovery.
- NestJS se crea dentro del proceso de las suites, no en `globalSetup`.
- `forceExit` permanece desactivado para no ocultar fugas de recursos.
- Solo el principal posee aplicación, base y teardown global.
- La base es real, temporal, aislada y migrada.
- Los fixtures usan HTTP salvo seed justificado.
- Los flujos autenticados obtienen tokens por HTTP.
- No se permiten mocks internos ni bypass de persistencia.
- La excepción externa sustituye el adaptador, no la lógica de aplicación.
- El ejemplo de correo reconoce que no prueba entregabilidad.
- Los contratos verifican ausencia de secretos.

## 12. Matriz de trazabilidad

| Decisión acordada                  | Artefacto propietario                            | Evidencia                                          |
| ---------------------------------- | ------------------------------------------------ | -------------------------------------------------- |
| E2E ejecuta implementación real    | `e2e-run-real-application-and-infrastructure.md` | Eval atraviesa HTTP, providers y base reales       |
| Bootstrap replica producción       | `e2e-run-real-application-and-infrastructure.md` | Ejemplo deriva configuración del bootstrap real    |
| PostgreSQL temporal y migraciones  | `e2e-run-real-application-and-infrastructure.md` | Harness crea, migra y elimina una base exclusiva   |
| Orquestador principal obligatorio  | `e2e-orchestrate-execution-and-lifecycle.md`     | Entry point registra funcionalidades en orden      |
| Orquestador por funcionalidad      | `e2e-orchestrate-execution-and-lifecycle.md`     | Cada módulo registra suites de endpoint            |
| Control del orden                  | `e2e-orchestrate-execution-and-lifecycle.md`     | No depende del orden de discovery                  |
| Discovery único de Jest            | `e2e-orchestrate-execution-and-lifecycle.md`     | `testMatch` descubre solo el principal             |
| Workers y concurrencia             | `e2e-orchestrate-execution-and-lifecycle.md`     | Sin `test.concurrent`; worker único es defensivo   |
| Setup de Jest y proceso de NestJS  | `e2e-orchestrate-execution-and-lifecycle.md`     | App creada en suite, no en `globalSetup`           |
| Contexto y cleanup tipados         | `e2e-orchestrate-execution-and-lifecycle.md`     | Ownership y cleanup inverso explícitos             |
| Datos por HTTP                     | `e2e-build-data-and-assert-contracts.md`         | Fixtures creados por endpoints disponibles         |
| Seeds excepcionales                | `e2e-build-data-and-assert-contracts.md`         | Cada seed incluye justificación                    |
| Payload válido canónico            | `e2e-build-data-and-assert-contracts.md`         | Fábrica/constante reutilizada sin mutación         |
| Contrato y secretos                | `e2e-build-data-and-assert-contracts.md`         | Status, schema y ausencia explícita                |
| Mock permitido para correo externo | `e2e-isolate-external-service-boundaries.md`     | Override del transport y contrato capturado        |
| Servicios internos reales          | `e2e-isolate-external-service-boundaries.md`     | Endpoint, aplicación y persistencia no sustituidos |
| Progressive disclosure             | `SKILL.md`                                       | Mapa carga solo tarjetas pertinentes               |
| Activación especializada           | Frontmatter y evals                              | Positivos NestJS E2E y near-misses negativos       |

## 13. Riesgos y mitigaciones

| Riesgo                                                  | Consecuencia                             | Mitigación                                                                          |
| ------------------------------------------------------- | ---------------------------------------- | ----------------------------------------------------------------------------------- |
| Duplicar reglas en `nestjs-practices`                   | Contradicciones y triggering ambiguo     | Migrar y eliminar en la misma unidad de trabajo                                     |
| Confundir orden de registro con dependencia entre tests | Suites frágiles                          | Datos independientes por caso y dependencias de flujo explícitas                    |
| Discovery ejecuta sub-suites además del principal       | Doble ejecución y cleanup competitivo    | Inspeccionar patrones y usar sufijo/ubicación excluidos                             |
| Jest usa defaults que descubren `*.spec.ts` importados  | Suites duplicadas y orden incontrolable  | Proyecto E2E con `testMatch` exclusivo para el principal                            |
| `runInBand` sustituye la orquestación                   | Orden aparente y arquitectura frágil     | Composición explícita; worker único solo como protección                            |
| NestJS se crea en `globalSetup`                         | La suite no puede acceder a la instancia | Crear/cerrar la app en el orquestador principal                                     |
| `forceExit` oculta handles abiertos                     | Fugas de pools, transports o servidores  | Mantenerlo desactivado y corregir el teardown                                       |
| Teardown no corre tras fallo de setup                   | Bases y procesos filtrados               | `try/finally`, handles idempotentes y cleanup parcial                               |
| El harness apunta a desarrollo o producción             | Pérdida de datos                         | Validación estricta de URL y allowlist E2E antes de operaciones destructivas        |
| La excepción de correo se expande a servicios internos  | Falso E2E                                | Override exclusivo del token del adaptador y eval adversarial                       |
| Ejemplos hacen obligatorios Fastify o Prisma            | Menor portabilidad                       | Condicionar ejemplos a la tecnología detectada                                      |
| Cuatro tarjetas se vuelven monolíticas                  | Sobrecarga cognitiva                     | Revisar cohesión por contexto y extraer solo decisiones independientes              |
| La descripción sobre-activa                             | Ruido en unit tests o frontend E2E       | Evals negativos cercanos y optimización con conjunto reservado                      |
| La base por ejecución aumenta tiempo                    | Feedback lento                           | Reutilizar una base dentro del orquestador principal, aislar datos y medir duración |

## 14. Unidades de trabajo

### Unidad 1. Esqueleto y reglas canónicas

- Crear nueva skill y cuatro tarjetas.
- Migrar contenido E2E válido.
- Añadir reglas nuevas de principal, base aislada y frontera externa.
- Incluir ejemplos y fuentes.

**Verificación enfocada:** `quick_validate.py` sobre la nueva skill y revisión de enlaces.

**Rollback:** eliminar únicamente `skills/typescript/nestjs-e2e-practices/`; todavía no se modifica
el catálogo anterior.

### Unidad 2. Transferencia de propiedad y registro

- Retirar E2E de `nestjs-practices`.
- Eliminar seis tarjetas reemplazadas.
- Actualizar ambos README, README raíz y marketplace.

**Verificación enfocada:** inventarios, marketplace y ausencia de enlaces rotos.

**Rollback:** restaurar navegación/tarjetas anteriores y retirar registros de la nueva skill sin
afectar sus archivos, si se necesita revisar la migración.

### Unidad 3. Evals e iteración

- Crear evals.
- Ejecutar comparación, grading, benchmark y viewer.
- Ajustar reglas o descripción según evidencia.

**Verificación enfocada:** assertions y revisión humana.

**Rollback:** revertir únicamente cambios derivados de la iteración, conservando el draft validado.

### Unidad 4. Validación integral

- Ejecutar validadores completos.
- Revisar trazabilidad, riesgos y diff.
- Preparar entrega.

**Verificación enfocada:** `pnpm validate` y checklist final.

**Rollback:** no aplica como cambio funcional; cualquier corrección vuelve a la unidad propietaria.

## 15. Criterios de aceptación

- Existe `skills/typescript/nestjs-e2e-practices/SKILL.md` y su nombre coincide con el directorio.
- La skill se activa ante creación, revisión y corrección de E2E NestJS.
- La skill no se activa ante unit tests, frontend E2E o testing genérico.
- `SKILL.md` funciona como mapa y las reglas detalladas viven en cuatro tarjetas coherentes.
- Hay un orquestador principal y un orquestador por funcionalidad en la arquitectura recomendada.
- El orden se controla por registro explícito, no por discovery o nombres.
- La configuración Jest E2E descubre únicamente `main.e2e-spec.ts` o su equivalente local.
- Las sub-suites usan un patrón excluido del discovery directo.
- Los flujos compartidos no usan `test.concurrent`.
- `maxWorkers: 1` o `--runInBand` se documenta como protección, no como fuente del orden.
- La aplicación NestJS no se crea en `globalSetup` ni en `setupFilesAfterEnv`.
- `forceExit` permanece desactivado y los handles abiertos se corrigen mediante teardown.
- El principal posee bootstrap, base, migraciones y teardown.
- La aplicación y componentes internos se ejecutan de forma real.
- La persistencia usa una base temporal aislada y nunca desarrollo o producción.
- Los datos se crean por HTTP; cada seed tiene una justificación verificable.
- Payloads inválidos derivan de bases válidas sin mutación compartida.
- Assertions cubren contratos públicos, errores, cabeceras, efectos y secretos ausentes.
- El envío externo de correo puede sustituirse solo en el adaptador de borde.
- Cada sustitución externa se reporta con motivo y limitación residual.
- Las seis tarjetas E2E antiguas dejan de existir y no quedan referencias rotas.
- README raíz y marketplace registran la nueva skill.
- Evals comparativos y triggering reciben revisión humana.
- `quick_validate.py` y `pnpm validate` terminan correctamente.
- No se crea commit ni push sin solicitud explícita.

## 16. Checklist ejecutable

### Preparación

- [x] Registrar estado y diff inicial.
- [x] Ejecutar validación baseline.
- [x] Crear snapshot para comparación.
- [x] Mapear las seis tarjetas E2E existentes.
- [x] Verificar documentación oficial y versiones relevantes.

### Skill y tarjetas

- [x] Crear `nestjs-e2e-practices/SKILL.md`.
- [x] Crear README de inventario.
- [x] Crear tarjeta de orquestación y lifecycle.
- [x] Incluir configuración Jest E2E con discovery exclusivo del principal.
- [x] Documentar workers, concurrencia, `globalSetup`, `setupFilesAfterEnv` y `forceExit`.
- [x] Crear tarjeta de aplicación e infraestructura reales.
- [x] Crear tarjeta de datos y contratos.
- [x] Crear tarjeta de fronteras externas.
- [x] Verificar atomicidad por contexto y ausencia de duplicación.
- [x] Verificar ejemplos incorrecto/correcto y fuentes oficiales.

### Migración y registro

- [x] Retirar E2E de `nestjs-practices/SKILL.md`.
- [x] Retirar E2E de `nestjs-practices/README.md`.
- [x] Eliminar las seis tarjetas migradas.
- [x] Añadir la skill al README raíz.
- [x] Añadir la skill al marketplace TypeScript.
- [x] Confirmar que no quedan enlaces rotos.

### Evals

- [x] Crear `evals/evals.json` con casos realistas.
- [x] Ejecutar runs con skill y baseline simultáneamente.
- [x] Definir assertions objetivas.
- [ ] Capturar tiempos y tokens (el runtime no los expuso; la limitación quedó documentada en el
      benchmark).
- [x] Generar grading y benchmark en el workspace externo
      `../nestjs-e2e-practices-workspace/iteration-1/`.
- [x] Generar el viewer oficial de `skill-creator` en
      `../nestjs-e2e-practices-workspace/iteration-1/review.html`.
- [x] Recoger revisión humana; el usuario aceptó los resultados iniciales y la iteración de OpenCode
      añadió un límite generalizable para APIs desplegadas sin acceso al código.
- [x] Evaluar y optimizar triggering con positivos y near-misses en OpenCode `1.18.4`: `20/20` en 60
      runs; el loop oficial de Claude no aplica a este entorno.

### Cierre

- [x] Ejecutar ambos validadores enfocados.
- [x] Ejecutar `pnpm validate`.
- [x] Confirmar matriz de trazabilidad.
- [x] Confirmar criterios de aceptación; aceptación formal recibida del usuario.
- [x] Revisar diff completo y preservar cambios ajenos.
- [x] Entregar resultados y riesgos residuales sin commit automático.
