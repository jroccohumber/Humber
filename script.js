const providers = [
  "Logistica Andina SA",
  "Transporte del Pacifico",
  "Rutas del Mercosur",
  "Flete Austral Ltda",
  "Cargo Norte Express",
  "Operador Rio Grande",
  "Camino Federal SRL",
  "Servicios Ruta Sur",
  "Latam Trucking Group",
  "Pampa Logistics",
  "Andes Supply Chain",
  "Cordillera Cargo",
];

const trips = [
  {
    crt: "008812102FSNACL",
    mic: "25CL445410C",
    travelDate: "05/03/2026",
    plant: "TRADEX INTERNATIONAL SRL",
    transportista: "ZANASSI FLAVIA ESTEFANY",
    chofer: "SEGUNDO SANCHEZ JOSE JOEL",
    camion: "AD00LY",
    semi: "AD227FW",
    costs: [
      {
        id: "85",
        date: "04/03/2026",
        type: "ATA",
        qty: "1",
        amount: "$ 60,00",
        subtotal: "$ 60,00",
        instant: "No",
        limit: "11/03/2026",
      },
      {
        id: "86",
        date: "04/03/2026",
        type: "Puerto",
        qty: "1",
        amount: "$ 57,31",
        subtotal: "$ 57,31",
        instant: "No",
        limit: "11/03/2026",
      },
    ],
  },
  {
    crt: "00861210MFSNACL",
    mic: "25CL778209",
    travelDate: "04/03/2026",
    plant: "TRADEX INTERNATIONAL SRL",
    transportista: "SAMASA R. L.",
    chofer: "LUIS ORTIZ",
    camion: "AH15EV",
    semi: "AG369EC",
    costs: [],
  },
  {
    crt: "07T pruiw0",
    mic: "24ZR4675E",
    travelDate: "04/03/2026",
    plant: "TRADEX INTERNATIONAL SRL",
    transportista: "MALVONI HUGO AMERICO",
    chofer: "ARCE CARLOS ALBERTO",
    camion: "KFB379",
    semi: "AF229LN",
    costs: [],
  },
  {
    crt: "0010004206FBS ARG",
    mic: "26AR0656ST",
    travelDate: "03/03/2026",
    plant: "QUIROMAS CHILE SPA",
    transportista: "GUERRA SHELAR ADRIANA",
    chofer: "NOE ALEJO AGUSTIN",
    camion: "MAB885",
    semi: "AB596LX",
    costs: [],
  },
  {
    crt: "0020095026FBS ARG",
    mic: "26AR08123X",
    travelDate: "03/03/2026",
    plant: "ADECOAGRO CHILE SPA",
    transportista: "MALVONI HUGO AMERICO",
    chofer: "OROZCO MIGUEL ANGEL",
    camion: "KYB379",
    semi: "AF223JL",
    costs: [],
  },
  {
    crt: "0020059206FBSARG",
    mic: "26AR091010",
    travelDate: "03/03/2026",
    plant: "ADECOAGRO CHILE SPA",
    transportista: "MALVONI HUGO AMERICO",
    chofer: "NORIEGA PABLO SEBASTIAN",
    camion: "GHF308",
    semi: "MPU838",
    costs: [],
  },
  {
    crt: "0020017105FBSARG",
    mic: "26AR24475P",
    travelDate: "03/03/2026",
    plant: "TRADEX INTERNATIONAL SRL",
    transportista: "MALVONI HUGO AMERICO",
    chofer: "BASTIAN MARIO ALEJANDRO",
    camion: "FGT167",
    semi: "AG884JK",
    costs: [],
  },
  {
    crt: "0020071205FBSARG",
    mic: "26AR24751L",
    travelDate: "02/03/2026",
    plant: "TRADEX INTERNATIONAL SRL",
    transportista: "MALVONI HUGO AMERICO",
    chofer: "ARCE CARLOS ALBERTO",
    camion: "KTM780",
    semi: "KJI971",
    costs: [],
  },
  {
    crt: "0010095302FBSARG",
    mic: "25AR451825Y",
    travelDate: "28/02/2026",
    plant: "QUIROMAS CHILE SPA",
    transportista: "ABRUT MARCELO EDGARDO",
    chofer: "BASTIAN MARIO ALEJANDRO",
    camion: "JAC204",
    semi: "AH113FBO",
    costs: [],
  },
  {
    crt: "00100643205FBSARG",
    mic: "25AR451819Y",
    travelDate: "28/02/2026",
    plant: "QUIROMAS CHILE SPA",
    transportista: "MOLINA DAVID MANUEL",
    chofer: "LOPEZ LEONEL",
    camion: "AGB4LK",
    semi: "FGT167",
    costs: [],
  },
];

function shuffle(list) {
  const clone = [...list];

  for (let index = clone.length - 1; index > 0; index -= 1) {
    const randomIndex = Math.floor(Math.random() * (index + 1));
    [clone[index], clone[randomIndex]] = [clone[randomIndex], clone[index]];
  }

  return clone;
}

function renderCosts(costs, container) {
  const costTemplate = document.getElementById("cost-row-template");
  const total = costs.reduce((sum, cost) => {
    const normalizedValue = Number(
      cost.subtotal
        .replace("$", "")
        .replace(/\./g, "")
        .replace(",", ".")
        .trim()
    );

    return sum + normalizedValue;
  }, 0);

  costs.forEach((cost) => {
    const fragment = costTemplate.content.cloneNode(true);
    fragment.querySelector(".cost-id").textContent = cost.id;
    fragment.querySelector(".cost-date").textContent = cost.date;
    fragment.querySelector(".cost-type").textContent = cost.type;
    fragment.querySelector(".cost-qty").textContent = cost.qty;
    fragment.querySelector(".cost-amount").textContent = cost.amount;
    fragment.querySelector(".cost-subtotal").textContent = cost.subtotal;
    fragment.querySelector(".cost-instant").textContent = cost.instant;
    fragment.querySelector(".cost-limit").textContent = cost.limit;
    container.appendChild(fragment);
  });

  if (costs.length > 0) {
    const totalRow = document.createElement("tr");
    const formattedTotal = total.toLocaleString("es-AR", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
    totalRow.innerHTML = `
      <td colspan="5"></td>
      <td class="currency-cell total-cell">
        <span class="currency-badge">USD</span>
        <strong>$ ${formattedTotal}</strong>
      </td>
      <td colspan="4"></td>
    `;
    container.appendChild(totalRow);
  }
}

function renderTrips() {
  const tripTemplate = document.getElementById("trip-row-template");
  const tripRows = document.getElementById("trip-rows");
  const randomizedProviders = shuffle(providers);

  trips.forEach((trip, index) => {
    const providerName = randomizedProviders[index % randomizedProviders.length];
    const fragment = tripTemplate.content.cloneNode(true);

    const tripRow = fragment.querySelector(".trip-row");
    const detailsRow = fragment.querySelector(".details-row");
    const toggleButton = fragment.querySelector(".toggle-button");
    const providerPill = fragment.querySelector(".provider-pill");

    providerPill.textContent = providerName;
    fragment.querySelector(".crt").textContent = trip.crt;
    fragment.querySelector(".mic").textContent = trip.mic;
    fragment.querySelector(".travel-date").textContent = trip.travelDate;
    fragment.querySelector(".plant").textContent = trip.plant;
    fragment.querySelector(".transportista").textContent = trip.transportista;
    fragment.querySelector(".chofer").textContent = trip.chofer;
    fragment.querySelector(".camion").textContent = trip.camion;
    fragment.querySelector(".semi").textContent = trip.semi;

    if (trip.costs.length > 0) {
      const costBody = fragment.querySelector(".cost-body");
      renderCosts(trip.costs, costBody);
    } else {
      detailsRow.remove();
      toggleButton.disabled = true;
      toggleButton.classList.add("is-disabled");
    }

    const shouldExpand = index === 0 && trip.costs.length > 0;
    toggleButton.setAttribute("aria-expanded", String(shouldExpand));

    if (trip.costs.length > 0) {
      detailsRow.hidden = !shouldExpand;

      toggleButton.addEventListener("click", () => {
        const isExpanded = toggleButton.getAttribute("aria-expanded") === "true";
        toggleButton.setAttribute("aria-expanded", String(!isExpanded));
        detailsRow.hidden = isExpanded;
        tripRow.classList.toggle("is-open", !isExpanded);
      });
    }

    tripRow.classList.toggle("is-open", shouldExpand);
    tripRows.appendChild(fragment);
  });
}

renderTrips();
