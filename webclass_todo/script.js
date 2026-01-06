$(document).ready(function() {
    let todos = [];
    let currentFilter = 'all';

    $('#addBtn').on('click', addTodo);
    $('#todoInput').on('keypress', function(e) {
        if (e.which === 13) addTodo();
    });

    function addTodo() {
        const text = $('#todoInput').val().trim();
        if (!text) return;

        todos.push({
            id: Date.now(),
            text: text,
            completed: false
        });

        $('#todoInput').val('');
        render();
    }

    $('#todoList').on('change', '.todo-checkbox', function() {
        const id = $(this).closest('.todo-item').data('id');
        const todo = todos.find(t => t.id === id);
        if (todo) {
            todo.completed = !todo.completed;
            render();
        }
    });

    $('#todoList').on('click', '.delete-btn', function() {
        const id = $(this).closest('.todo-item').data('id');
        todos = todos.filter(t => t.id !== id);
        render();
    });

    $('.filter-btn').on('click', function() {
        $('.filter-btn').removeClass('active');
        $(this).addClass('active');
        currentFilter = $(this).data('filter');
        render();
    });

    function render() {
        const $list = $('#todoList');
        $list.empty();
        let filtered = todos;
        if (currentFilter === 'active') filtered = todos.filter(t => !t.completed);
        if (currentFilter === 'completed') filtered = todos.filter(t => t.completed);

        if (filtered.length === 0) {
            $list.html('<div class="empty-state"><p>No tasks</p></div>');
        } else {
            filtered.forEach(todo => {
                $list.append(`
                    <li class="todo-item ${todo.completed ? 'completed' : ''}" data-id="${todo.id}">
                        <input type="checkbox" class="todo-checkbox" ${todo.completed ? 'checked' : ''}>
                        <span class="todo-text">${$('<div>').text(todo.text).html()}</span>
                        <button class="delete-btn">Delete</button>
                    </li>
                `);
            });
        }
        const total = todos.length;
        const completed = todos.filter(t => t.completed).length;
        const active = total - completed;
        $('#statsText').text(total === 0 ? 'No tasks' : `${active} active, ${completed} completed`);
    }

    render();
});