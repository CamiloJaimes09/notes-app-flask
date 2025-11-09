let notaIdAEliminar = null;

function abrirModalEliminar(id, titulo) {
    notaIdAEliminar = id;
    
    document.getElementById('textoModal').textContent = 
        `¿Estás seguro de que quieres eliminar la nota "${titulo}"?`;
    
    const form = document.getElementById('formEliminar');
    form.action = `/eliminar-nota/${id}`;
    
    document.getElementById('modalEliminar').style.display = 'block';
}

function cerrarModal() {
    document.getElementById('modalEliminar').style.display = 'none';
    notaIdAEliminar = null;
}

document.addEventListener('click', function(event) {
    const modal = document.getElementById('modalEliminar');
    if (event.target === modal) {
        cerrarModal();
    }
});

document.querySelectorAll('.btn-eliminar').forEach(btn => {
    btn.addEventListener('click', function() {
        const id = this.getAttribute('data-id');
        const title = this.getAttribute('data-title');
        abrirModalEliminar(id, title);
    });
});