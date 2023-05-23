<template>
    <div>
        <div v-if="showModal" class="modal">
            <div class="modal-content">
                <span class="close" @click="closeModal">&times;</span>
                <h2>VOTRE RÉSULTAT</h2>
                <p> CO2: {{ score.co2 }} g/km </p>
                <div class="co2-graphic" :style="{
                  height: 300 * (score.co2/150) + 'px'}">
                  <img class="cloud-img" src="../assets/co2-emissions.png" alt="cloud"/>
                </div>
                <p> Temps d'attente: {{ score.wait }} secondes</p>
                <h2>LE RÉSULTAT DE L'AI</h2>
                <p> CO2: {{ aiScore.co2 }} g/km </p>
                <div class="co2-graphic" :style="{
                  height: 300 * (aiScore.co2/150) + 'px'}">
                  <img class="cloud-img" src="../assets/co2-emissions.png" alt="cloud"/>
                </div>
                <p> Temps d'attentes: {{ aiScore.wait }} secondes</p>
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
    },
    score: {
      default: {
        co2: 0,
        wait: 0
      }
    },
    aiScore: {
      default: {
        co2: 0,
        wait: 0
      }
    }
  },
  methods: {
    closeModal() {
      this.$emit('close-modal');
    },
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
    width: 500px;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
    background-color: #fefefe;
    margin: 15% auto;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
    height: 80%;
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

.co2-graphic {
    width: 50px;
    margin-bottom: 10px;
}

.cloud-img {
  height: 100%;
}
</style>
