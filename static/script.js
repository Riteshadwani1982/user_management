const API_URL = 'http://localhost:5000/users';

// Fetch and display users
function fetchUsers() {
  fetch(API_URL)
    .then(res => res.json())
    .then(data => {
      const tbody = document.querySelector('#users-table tbody');
      tbody.innerHTML = '';
      data.forEach(user => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${user.name}</td>
          <td>${user.email}</td>
          <td>${user.age}</td>
          <td>
            <button class="action-btn" onclick="editUser(${user.id})">Edit</button>
            <button class="action-btn" onclick="deleteUser(${user.id})">Delete</button>
          </td>
        `;
        tbody.appendChild(row);
      });
    })
    .catch(err => console.error('Error fetching users:', err));
}

// Add or update a user
document.getElementById('user-form').addEventListener('submit', function (e) {
  e.preventDefault();
  const id = document.getElementById('user-id').value;
  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const age = document.getElementById('age').value;

  const userData = { name, email, age };

  // Determine whether to create or update
  if (id) {
    // Update
    fetch(`${API_URL}/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    })
      .then(() => {
        resetForm();
        fetchUsers();
      })
      .catch(err => console.error('Error updating user:', err));
  } else {
    // Create
    fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    })
      .then(() => {
        resetForm();
        fetchUsers();
      })
      .catch(err => console.error('Error adding user:', err));
  }
});

function resetForm() {
  document.getElementById('user-form').reset();
  document.getElementById('user-id').value = '';
}

// Fill form with user data for editing
function editUser(id) {
  fetch(`${API_URL}/${id}`)
    .then(res => res.json())
    .then(user => {
      document.getElementById('user-id').value = user.id;
      document.getElementById('name').value = user.name;
      document.getElementById('email').value = user.email;
      document.getElementById('age').value = user.age;
    })
    .catch(err => console.error('Error fetching user:', err));
}

// Delete a user
function deleteUser(id) {
  fetch(`${API_URL}/${id}`, {
    method: 'DELETE'
  })
    .then(() => fetchUsers())
    .catch(err => console.error('Error deleting user:', err));
}

// Initial load
fetchUsers();
