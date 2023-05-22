<template>
    <div>
        <div v-if="showModal" class="modal">
            <div class="modal-content">
                <span class="close" @click="closeModal">&times;</span>
                <h2>Result Title Section</h2>
                <p>You're pretty good !.</p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        showModal: {
            type: Boolean,
            default: false
        }
    },
    methods: {
        closeModal() {
            this.$emit('close-modal');
        }
    }
};
</script>

<style>
.modal {
    display: block;
    position: fixed;
    z-index: 9999;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
    background-color: #fefefe;
    margin: 15% auto;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
}

.close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
}

.close:hover,
.close:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
}
</style>
