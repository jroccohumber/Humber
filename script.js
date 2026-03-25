const slides = [
  {
    number: "01",
    kind: "Portada",
    file: "slides/01-portada.svg",
    title: "Metodología Scrum aplicada a Humber",
    description:
      "Carátula principal para abrir la exposición con contexto, identidad de marca y foco en el marco Scrum.",
    points: [
      "Introduce el objetivo de la charla.",
      "Presenta la relación entre Scrum y Humber.",
      "Sirve como arranque visual limpio y profesional.",
    ],
  },
  {
    number: "02",
    kind: "Vista general",
    file: "slides/02-mapa-scrum.svg",
    title: "Mapa de ceremonias Scrum",
    description:
      "Vista panorámica del ciclo para ubicar todas las ceremonias dentro de una misma narrativa.",
    points: [
      "Muestra cuándo ocurre cada evento.",
      "Ayuda a conectar flujo, inspección y adaptación.",
      "Ideal para anticipar lo que vas a explicar después.",
    ],
  },
  {
    number: "03",
    kind: "Marco base",
    file: "slides/03-el-sprint.svg",
    title: "El Sprint como contenedor",
    description:
      "Lámina puente para contar que el sprint contiene todos los eventos y ordena la entrega de valor.",
    points: [
      "Explica la duración recomendada del sprint.",
      "Refuerza el Sprint Goal como eje del trabajo.",
      "Muestra cómo conviven planning, daily, review y retro.",
    ],
  },
  {
    number: "04",
    kind: "Ceremonia 01",
    file: "slides/04-sprint-planning.svg",
    title: "Sprint Planning",
    description:
      "Ceremonia de inicio donde se define el objetivo del sprint, el alcance y el plan de trabajo.",
    points: [
      "Define por qué el sprint es valioso.",
      "Aterriza prioridades y capacidad real.",
      "Deja como salida el Sprint Goal y el Sprint Backlog.",
    ],
  },
  {
    number: "05",
    kind: "Ceremonia 02",
    file: "slides/05-daily-scrum.svg",
    title: "Daily Scrum",
    description:
      "Instancia diaria de sincronización para inspeccionar el progreso y ajustar el plan del equipo.",
    points: [
      "Debe ser breve, concreta y diaria.",
      "Detecta impedimentos tempranamente.",
      "No es un reporte al jefe, sino coordinación del equipo.",
    ],
  },
  {
    number: "06",
    kind: "Práctica recomendada",
    file: "slides/06-backlog-refinement.svg",
    title: "Backlog Refinement",
    description:
      "Práctica continua que mejora la calidad de las historias antes de comprometerlas en planning.",
    points: [
      "Aclara alcance, criterios y dependencias.",
      "Reduce incertidumbre antes del sprint.",
      "Ayuda a llegar más preparados a la planificación.",
    ],
  },
  {
    number: "07",
    kind: "Ceremonia 03",
    file: "slides/07-sprint-review.svg",
    title: "Sprint Review",
    description:
      "Espacio para demostrar el incremento y recoger feedback real del negocio y stakeholders.",
    points: [
      "Se revisa trabajo terminado y usable.",
      "La conversación gira en torno al producto.",
      "El backlog puede adaptarse con lo aprendido.",
    ],
  },
  {
    number: "08",
    kind: "Ceremonia 04",
    file: "slides/08-sprint-retrospective.svg",
    title: "Sprint Retrospective",
    description:
      "Momento de reflexión del equipo sobre cómo trabajó y qué mejoras llevará al próximo sprint.",
    points: [
      "Busca aprendizaje, no culpables.",
      "Conviene cerrar con acciones concretas.",
      "Conecta la mejora continua con la siguiente planning.",
    ],
  },
];

function createPoints(points) {
  return points.map((point) => `<li>${point}</li>`).join("");
}

function createSlideCard(slide) {
  const article = document.createElement("article");
  article.className = "slide-card";

  article.innerHTML = `
    <a class="slide-preview" href="./${slide.file}" target="_blank" rel="noreferrer">
      <img src="./${slide.file}" alt="${slide.title}" loading="lazy" />
    </a>
    <div class="slide-content">
      <div class="slide-meta">
        <span class="slide-number">Slide ${slide.number}</span>
        <span class="slide-kind">${slide.kind}</span>
      </div>
      <h3 class="slide-title">${slide.title}</h3>
      <p class="slide-description">${slide.description}</p>
      <ul class="slide-points">
        ${createPoints(slide.points)}
      </ul>
      <div class="slide-actions">
        <a class="button is-primary" href="./${slide.file}" target="_blank" rel="noreferrer">Abrir SVG</a>
      </div>
    </div>
  `;

  return article;
}

function renderSlides() {
  const grid = document.getElementById("slides-grid");

  slides.forEach((slide) => {
    grid.appendChild(createSlideCard(slide));
  });
}

renderSlides();
