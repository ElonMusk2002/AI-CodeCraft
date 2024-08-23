document.addEventListener("DOMContentLoaded", () => {
  initializeProfileFormToggle();
  initializeChallengeForms();
  initializeShowMoreButtons();
  initializeGenerateChallengeButton();
  initializeSmoothScroll();
  initializeScrollAnimations();
  initializeChallengeCardHoverEffects();
  initializeTypewriterEffect();
});

function initializeProfileFormToggle() {
  const profileFormBtn = document.getElementById("profile-form-btn");
  const profileForm = document.getElementById("profile-form");

  if (profileFormBtn && profileForm) {
    profileFormBtn.addEventListener("click", () => {
      profileForm.classList.toggle("hidden");
    });
  }
}

function initializeChallengeForms() {
  const challengeForms = document.querySelectorAll(".challenge-form");

  challengeForms.forEach((form) => {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();

      const formData = new FormData(form);
      const actionUrl = form.action;

      try {
        const response = await fetch(actionUrl, {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          const jsonResponse = await response.json();
          handleChallengeResponse(jsonResponse, form);
        } else {
          throw new Error("Error submitting your solution.");
        }
      } catch (error) {
        handleError(error);
      }
    });
  });
}

function handleChallengeResponse(jsonResponse, form) {
  if (jsonResponse.status === "success") {
    const button = form.previousElementSibling;
    button.classList.add("disabled");
    button.textContent = "Completed";
    form.classList.add("hidden");
  } else {
    alert("Error submitting your solution. Please try again.");
  }
}

function initializeShowMoreButtons() {
  const showMoreButtons = document.querySelectorAll(".show-more-btn");

  showMoreButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const card = button.closest(".challenge-card");
      card.classList.toggle("show-more-expanded");
      button.textContent = card.classList.contains("show-more-expanded")
        ? "Show Less"
        : "Show More";
    });
  });
}

function initializeGenerateChallengeButton() {
  const generateChallengeBtn = document.getElementById(
    "generate-challenge-btn"
  );
  const challengeContainer = document.getElementById("challenge-container");

  if (generateChallengeBtn) {
    generateChallengeBtn.addEventListener("click", async () => {
      try {
        const response = await fetch("/recommend", {
          method: "GET",
        });

        if (response.ok) {
          const challenge = await response.json();
          const challengeCard = createChallengeCard(challenge);

          challengeContainer.innerHTML = "";
          challengeContainer.appendChild(challengeCard);

          challengeCard.classList.add("fade-in");
        } else {
          throw new Error("Error generating a new coding challenge.");
        }
      } catch (error) {
        handleError(error);
      }
    });
  }
}

function handleError(error) {
  console.error("Error:", error);
  alert("An error occurred. Please try again later.");
}

function initializeSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      document.querySelector(this.getAttribute("href")).scrollIntoView({
        behavior: "smooth",
      });
    });
  });
}

function initializeScrollAnimations() {
  const animateOnScroll = () => {
    const elements = document.querySelectorAll(".animate-on-scroll");
    elements.forEach((element) => {
      const elementTop = element.getBoundingClientRect().top;
      const elementBottom = element.getBoundingClientRect().bottom;
      if (elementTop < window.innerHeight && elementBottom > 0) {
        element.classList.add("animate");
      }
    });
  };

  window.addEventListener("scroll", animateOnScroll);
  animateOnScroll();
}

function initializeChallengeCardHoverEffects() {
  const challengeCards = document.querySelectorAll(".challenge-card");
  challengeCards.forEach((card) => {
    card.addEventListener("mouseenter", () => {
      card.style.transform = "translateY(-5px)";
      card.style.boxShadow = "0 15px 40px rgba(0, 0, 0, 0.2)";
    });
    card.addEventListener("mouseleave", () => {
      card.style.transform = "translateY(0)";
      card.style.boxShadow = "0 10px 30px rgba(0, 0, 0, 0.1)";
    });
  });
}

function initializeTypewriterEffect() {
  const heroTitle = document.querySelector(".hero h1");
  if (heroTitle) {
    const text = heroTitle.textContent;
    heroTitle.textContent = "";
    let i = 0;
    const typeWriter = () => {
      if (i < text.length) {
        heroTitle.textContent += text.charAt(i);
        i++;
        setTimeout(typeWriter, 100);
      }
    };
    typeWriter();
  }
}

function createChallengeCard(challenge) {
  const card = document.createElement("div");
  card.classList.add("challenge-card");

  const title = document.createElement("h3");
  title.textContent = challenge.title;

  const description = document.createElement("p");
  description.textContent = `Description: ${challenge.description}`;

  const difficulty = document.createElement("p");
  difficulty.textContent = `Difficulty: ${challenge.difficulty}`;

  const language = document.createElement("p");
  language.textContent = `Programming Language: ${challenge.programming_language}`;

  const topic = document.createElement("p");
  topic.textContent = `Topic: ${challenge.topic}`;

  const completeButton = document.createElement("button");
  completeButton.classList.add("show-solution-form");
  completeButton.dataset.challengeId = challenge.id;
  completeButton.textContent = "Complete";

  const form = document.createElement("form");
  form.classList.add("challenge-form", "hidden");
  form.dataset.challengeId = challenge.id;
  form.action = `/complete/${challenge.id}`;
  form.method = "post";

  const textarea = document.createElement("textarea");
  textarea.name = "solution";
  textarea.placeholder = "Enter your solution here";
  textarea.rows = "4";
  textarea.cols = "50";

  const submitButton = document.createElement("button");
  submitButton.type = "submit";
  submitButton.textContent = "Submit Solution";

  form.appendChild(textarea);
  form.appendChild(submitButton);

  card.appendChild(title);
  card.appendChild(difficulty);
  card.appendChild(language);
  card.appendChild(topic);
  card.appendChild(description);
  card.appendChild(completeButton);
  card.appendChild(form);

  completeButton.addEventListener("click", () => {
    form.classList.toggle("hidden");
  });

  return card;
}
