document.getElementById('uploadBtn').addEventListener('click', async function() {
    const input = document.getElementById('folderInput');
    const files = Array.from(input.files);

    if (files.length === 0) {
        alert('Select a folder first.');
        return;
    }

    const formData = new FormData();
    files.forEach(f => formData.append('files', f));
    formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);

    const response = await fetch('/api/upload/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    });

    const data = await response.json();

    if (!response.ok) {
        alert(data.error);
    } else {
        loadFiles(data.fisiere);
    }
});

function loadFiles(fisiere) {
    const listaFisiere = document.getElementById('lista-fisiere');
    listaFisiere.innerHTML = '';
    fisiere.forEach(nume => {
        const label = document.createElement('label');
        label.classList.add('file-tag');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.value = nume;
        checkbox.name = 'selected_files';
        checkbox.checked = true;
        label.appendChild(checkbox);
        label.appendChild(document.createTextNode(' ' + nume));
        listaFisiere.appendChild(label);
    });

    const selectFile = document.getElementById('primary-file-select');
    selectFile.innerHTML = '';
    fisiere.forEach(nume => {
        const option = document.createElement('option');
        option.value = nume;
        option.textContent = nume;
        selectFile.appendChild(option);
    });

    loadSheets(fisiere[0]);
}

async function loadSheets(numeFisier) {
    const input = document.getElementById('folderInput');
    const file = Array.from(input.files).find(f => f.name === numeFisier);
    if (!file) return;

    const formData = new FormData();
    formData.append('primary_file', file);

    const response = await fetch('/api/sheets/', {
        method: 'POST',
        body: formData,
        headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value }
    });

    const data = await response.json();

    const selectSheet = document.getElementById('sheet-select');
    selectSheet.innerHTML = '';
    data.sheets.forEach(sheet => {
        const option = document.createElement('option');
        option.value = sheet;
        option.textContent = sheet;
        selectSheet.appendChild(option);
    });

    await getColumns(numeFisier, selectSheet.value);
}

// =====================
// CHANGE PRIMARY FILE
// =====================
document.getElementById('primary-file-select').addEventListener('change', function() {
    loadSheets(this.value);
});

// =====================
// CHANGE SHEET
// =====================
document.getElementById('sheet-select').addEventListener('change', async function() {
    const primaryFile = document.getElementById('primary-file-select').value;
    await getColumns(primaryFile, this.value);
});


async function getColumns(numeFisier, sheetName) {
    const input = document.getElementById('folderInput');
    const file = Array.from(input.files).find(f => f.name === numeFisier);
    if (!file) return;

    const formData = new FormData();
    formData.append('primary_file', file);
    formData.append('sheet_name', sheetName);

    const response = await fetch('/api/columns/', {
        method: 'POST',
        body: formData,
        headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value }
    });

    const data = await response.json();
    showColumns(data.columns);
}


function showColumns(columns) {
    const container = document.getElementById('columns-container');
    container.innerHTML = '';

    columns.forEach(col => {
        const label = document.createElement('label');
        label.style.display = 'block';

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.value = col;
        checkbox.name = 'selected_columns';
        checkbox.checked = true;

        label.appendChild(checkbox);
        label.appendChild(document.createTextNode(' ' + col));
        container.appendChild(label);
    });
}

// =====================
// MERGE
// =====================
document.getElementById('mergeBtn').addEventListener('click', async function() {
    const sheetName = document.getElementById('sheet-select').value;
    const primaryFileName = document.getElementById('primary-file-select').value;
    const outputFile = document.getElementById('outputFile').files[0];

    const selectedColumns = Array.from(
        document.querySelectorAll('input[name="selected_columns"]:checked')
    ).map(cb => cb.value);

    const selectedFiles = Array.from(
        document.querySelectorAll('input[name="selected_files"]:checked')
    ).map(cb => cb.value);

    if (selectedColumns.length === 0) {
        alert('Select at least one column.');
        return;
    }

    if (selectedFiles.length < 2) {
        alert('Select at least 2 files to merge.');
        return;
    }

    if (!outputFile) {
        alert('Select an output file.');
        return;
    }

    const input = document.getElementById('folderInput');
    const formData = new FormData();
    formData.append('sheet_name', sheetName);
    formData.append('primary_file_name', primaryFileName);
    formData.append('selected_columns', JSON.stringify(selectedColumns));
    formData.append('output_file', outputFile);

    Array.from(input.files)
        .filter(f => selectedFiles.includes(f.name))
        .forEach(f => formData.append('files', f));

    const response = await fetch('/api/merge/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    });

    if (!response.ok) {
        const data = await response.json();
        alert(data.error);
    } else {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = outputFile.name;
        a.click();
        window.URL.revokeObjectURL(url);
    }
});
