const API_URL = '/api/contacts'; // Nginx irá redirecionar /api/ para http://app:5000/

const contactForm = document.getElementById('contact-form');
const contactIdInput = document.getElementById('contact-id');
const nameInput = document.getElementById('name');
const phoneInput = document.getElementById('phone');
const emailInput = document.getElementById('email');
const submitButton = document.getElementById('submit-button');
const cancelEditButton = document.getElementById('cancel-edit-button');
const contactList = document.getElementById('contact-list');
const searchInput = document.getElementById('search-input');

// Função para buscar e exibir contatos
async function fetchContacts(searchTerm = '') {
    try {
        const response = await fetch(`${API_URL}?name=${searchTerm}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const contacts = await response.json();
        renderContacts(contacts);
    } catch (error) {
        console.error('Erro ao buscar contatos:', error);
        alert('Erro ao carregar contatos. Verifique a conexão com o backend.');
    }
}

// Função para renderizar a lista de contatos
function renderContacts(contacts) {
    contactList.innerHTML = '';
    if (contacts.length === 0) {
        contactList.innerHTML = '<p>Nenhum contato encontrado.</p>';
        return;
    }
    contacts.forEach(contact => {
        const li = document.createElement('li');
        li.innerHTML = `
            <div>
                <span>${contact.name}</span>
                <span>Telefone: ${contact.phone || 'N/A'}</span>
                <span>Email: ${contact.email || 'N/A'}</span>
            </div>
            <div class="contact-actions">
                <button class="edit-button" data-id="${contact.id}" data-name="${contact.name}" data-phone="${contact.phone}" data-email="${contact.email}">Editar</button>
                <button class="delete-button" data-id="${contact.id}">Excluir</button>
            </div>
        `;
        contactList.appendChild(li);
    });

    // Adiciona event listeners para os botões de editar e excluir
    document.querySelectorAll('.edit-button').forEach(button => {
        button.addEventListener('click', handleEditClick);
    });
    document.querySelectorAll('.delete-button').forEach(button => {
        button.addEventListener('click', handleDeleteClick);
    });
}

// Função para lidar com o envio do formulário (adicionar ou editar)
contactForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const id = contactIdInput.value;
    const name = nameInput.value.trim();
    const phone = phoneInput.value.trim();
    const email = emailInput.value.trim();

    if (!name) {
        alert('O nome é obrigatório!');
        return;
    }

    const contactData = { name, phone, email };

    try {
        let response;
        if (id) { // Editar contato existente
            response = await fetch(`${API_URL}/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(contactData)
            });
        } else { // Adicionar novo contato
            response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(contactData)
            });
        }

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        clearForm();
        fetchContacts(searchInput.value); // Atualiza a lista após a operação
        alert(id ? 'Contato atualizado com sucesso!' : 'Contato adicionado com sucesso!');
    } catch (error) {
        console.error('Erro ao salvar contato:', error);
        alert(`Erro ao salvar contato: ${error.message}`);
    }
});

// Função para preencher o formulário para edição
function handleEditClick(event) {
    const button = event.target;
    contactIdInput.value = button.dataset.id;
    nameInput.value = button.dataset.name;
    phoneInput.value = button.dataset.phone === 'N/A' ? '' : button.dataset.phone;
    emailInput.value = button.dataset.email === 'N/A' ? '' : button.dataset.email;

    submitButton.textContent = 'Atualizar Contato';
    cancelEditButton.style.display = 'inline-block';
}

// Função para cancelar a edição
cancelEditButton.addEventListener('click', () => {
    clearForm();
});

// Função para excluir um contato
async function handleDeleteClick(event) {
    const id = event.target.dataset.id;
    if (!confirm('Tem certeza que deseja excluir este contato?')) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        fetchContacts(searchInput.value); // Atualiza a lista
        alert('Contato excluído com sucesso!');
    } catch (error) {
        console.error('Erro ao excluir contato:', error);
        alert('Erro ao excluir contato.');
    }
}

// Função para limpar o formulário
function clearForm() {
    contactIdInput.value = '';
    nameInput.value = '';
    phoneInput.value = '';
    emailInput.value = '';
    submitButton.textContent = 'Adicionar Contato';
    cancelEditButton.style.display = 'none';
}

// Lidar com a pesquisa em tempo real
let searchTimeout;
searchInput.addEventListener('input', (event) => {
    clearTimeout(searchTimeout);
    const searchTerm = event.target.value;
    searchTimeout = setTimeout(() => {
        fetchContacts(searchTerm);
    }, 300); // Pequeno atraso para evitar muitas requisições
});

// Carrega os contatos ao iniciar a página
document.addEventListener('DOMContentLoaded', () => {
    fetchContacts();
});
