function showUpdateForm(id) {
    // Fetch the reservation data
    fetch(`/api/v1/reservations/api/reservations/${id}`)
        .then(response => response.json())
        .then(data => {
            // Populate the update form with the fetched data
            document.getElementById('update_id').value = data.id;
            const nameParts = data.guest_name.split(' ');
            document.getElementById('update_first_name').value = nameParts.slice(0, -1).join(' ');
            document.getElementById('update_last_name').value = nameParts[nameParts.length - 1];
            document.getElementById('update_email').value = data.email;
            document.getElementById('update_phone').value = data.phone;
            document.getElementById('update_check_in_date').value = data.checkin_date;
            document.getElementById('update_check_out_date').value = data.checkout_date;
            document.getElementById('update_room_number').value = data.room_number;

            // Show the update form
            document.getElementById('updateFormContainer').style.display = 'block';
        })
        .catch(error => console.error('Error fetching reservation:', error));
}

function hideUpdateForm() {
    document.getElementById('updateFormContainer').style.display = 'none';
}

function updateReservation() {
    const id = document.getElementById('update_id').value;
    const data = {
        guest_name: document.getElementById('update_first_name').value + " " + document.getElementById('update_last_name').value,
        email: document.getElementById('update_email').value,
        phone: document.getElementById('update_phone').value,
        checkin_date: document.getElementById('update_check_in_date').value,
        checkout_date: document.getElementById('update_check_out_date').value,
        room_number: document.getElementById('update_room_number').value
    };

    fetch(`/api/v1/reservations/api/update_reservations/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.message === "Reservation updated") {
            // Update the table row with the new data
            const row = document.getElementById(`reservation_${id}`);
            row.children[1].innerText = data.guest_name;
            row.children[2].innerText = data.email;
            row.children[3].innerText = data.phone;
            row.children[4].innerText = data.checkin_date;
            row.children[5].innerText = data.checkout_date;
            row.children[6].innerText = data.room_number;

            hideUpdateForm();
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function deleteReservation(id) {
    fetch(`/api/v1/reservations/api/delete_reservations/${id}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.message === "Reservation deleted") {
            // Remove the table row
            const row = document.getElementById(`reservation_${id}`);
            row.parentNode.removeChild(row);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
