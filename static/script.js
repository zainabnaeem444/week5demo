function showFilmDetails(filmId) {
    fetch(`/api/film/${filmId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error loading film details: ' + data.error);
                return;
            }

            const film = data.film;
            const actors = data.actors;
            
            let actorsHtml = '';
            if (actors && actors.length > 0) {
                actorsHtml = actors.map(actor => 
                    `<span class="badge bg-secondary me-1">${actor.first_name} ${actor.last_name}</span>`
                ).join('');
            } else {
                actorsHtml = '<span class="text-muted">No actors found</span>';
            }

            const modalContent = `
                <div class="row">
                    <div class="col-md-4">
                        <h6>Title</h6>
                        <p><strong>${film.title}</strong></p>
                        
                        <h6>Release Year</h6>
                        <p>${film.release_year || 'N/A'}</p>
                        
                        <h6>Category</h6>
                        <p>${film.category || 'N/A'}</p>
                        
                        <h6>Language</h6>
                        <p>${film.language_name || 'N/A'}</p>
                    </div>
                    <div class="col-md-4">
                        <h6>Rating</h6>
                        <p><span class="badge bg-info">${film.rating}</span></p>
                        
                        <h6>Length</h6>
                        <p>${film.length} minutes</p>
                        
                        <h6>Rental Duration</h6>
                        <p>${film.rental_duration} days</p>
                        
                        <h6>Rental Rate</h6>
                        <p>$${film.rental_rate}</p>
                    </div>
                    <div class="col-md-4">
                        <h6>Replacement Cost</h6>
                        <p>$${film.replacement_cost}</p>
                        
                        <h6>Special Features</h6>
                        <p>${film.special_features || 'N/A'}</p>
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col-12">
                        <h6>Description</h6>
                        <p>${film.description || 'No description available'}</p>
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col-12">
                        <h6>Actors</h6>
                        <div>${actorsHtml}</div>
                    </div>
                </div>
            `;

            document.getElementById('filmDetailsContent').innerHTML = modalContent;
            const modal = new bootstrap.Modal(document.getElementById('filmDetailsModal'));
            modal.show();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error loading film details');
        });
}

function editActor(actorId, firstName, lastName) {
    document.getElementById('edit_first_name').value = firstName;
    document.getElementById('edit_last_name').value = lastName;
    
    const form = document.getElementById('editActorForm');
    form.action = `/actors/edit/${actorId}`;
    
    const modal = new bootstrap.Modal(document.getElementById('editActorModal'));
    modal.show();
}

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});