const user = {
  name: "João da Silva",
  email: "joao@email.com",
  photoUrl: "default-profile.svg"
};

const quizzes = [
  { id: 1, title: "Quiz de Matemática", description: "Teste seus conhecimentos em matemática." },
  { id: 2, title: "Quiz de História", description: "Desafie-se com perguntas de história." }
];

function renderProfile() {
  const app = document.getElementById("app");
  app.innerHTML = `
    <div class="profile">
      <img src="${user.photoUrl}" alt="Foto de perfil" class="profile-photo" id="profilePhoto">
      <input type="file" id="photoInput" accept="image/*" style="display:none">
      <h2>${user.name}</h2>
      <p>${user.email}</p>
      <small>Clique na foto para alterar</small>
    </div>
  `;

  const photo = document.getElementById("profilePhoto");
  const input = document.getElementById("photoInput");
  photo.onclick = () => input.click();
  input.onchange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function(evt) {
        user.photoUrl = evt.target.result;
        renderProfile();
      };
      reader.readAsDataURL(file);
    }
  };
}

function renderQuizzes() {
  const app = document.getElementById("app");
  app.innerHTML = `
    <div>
      <h1>Quizzes</h1>
      <ul>
        ${quizzes.map(q => `
          <li>
            <strong>${q.title}</strong>
            <p>${q.description}</p>
          </li>
        `).join("")}
      </ul>
    </div>
  `;
}

document.getElementById("profileBtn").onclick = renderProfile;
document.getElementById("quizzesBtn").onclick = renderQuizzes;

// Página inicial
renderProfile();