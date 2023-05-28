<template>
  <div>
      <div v-if="showModal" class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <div class="title-container">
          <h2>VOTRE RÉSULTAT</h2>
          <img class="logo-img face-img" src="../assets/face.svg" alt="human"/>
        </div>
        <div class="scoreboard">
          <div class="scoreboard-item">
            <h3 class="score-label">CO2</h3>
            <p class="score-value">{{ score.co2 }} g</p>
          </div>
          <div class="scoreboard-item">
            <h3 class="score-label">Temps d'arrêt</h3>
            <p class="score-value">{{ score.wait }} secondes</p>
          </div>
        </div>
        <div class="containerImg">
          <img class="cloud-img" src="../assets/cloudversify.svg" alt="cloud" :style="{
            height: 120 * (score.co2/100) + 'px'}"/>
            <img class="car-img" src="../assets/co2-emissions.png" alt="car"/>
        </div>
        <div class="title-container">
          <h2>LE RÉSULTAT DE L'IA</h2>
          <img class="logo-img toy-img" src="../assets/toy.svg" alt="robot"/>
        </div>
        <div class="scoreboard">
          <div class="scoreboard-item">
            <h3 class="score-label">CO2</h3>
            <p class="score-value">{{ aiScore.co2 }} g</p>
          </div>
          <div class="scoreboard-item">
            <h3 class="score-label">Temps d'arrêt</h3>
            <p class="score-value">{{ aiScore.wait }} secondes</p>
          </div>
        </div>
        <div class="containerImg">
          <img class="cloud-img" src="../assets/cloudversify.svg" alt="cloud" :style="{
            height: 120 * (aiScore.co2/100) + 'px'}"/>
            <img class="car-img" src="../assets/co2-emissions.png" alt="car"/>
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

.modal-content {
    background-color: #fefefe;
    margin: 2%;
    padding: 20px;
    border: none;
    display: block;
    position: fixed;
    z-index: 9999;
    left: 0;
    top: 0;
    width: 400px;
    height: 90%;
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    border-radius: 18px;
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

.title-container {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
}
.containerImg{
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.face-img{
  filter: invert(8%) sepia(100%) saturate(7498%) hue-rotate(248deg) brightness(96%) contrast(145%);
}

.toy-img{
  filter: invert(10%) sepia(97%) saturate(5518%) hue-rotate(358deg) brightness(117%) contrast(114%);
}

.cloud-img {
  height: 100%;
  transform: rotate(180deg);
}

.car-img {
  width: 60%;
}

/* Scoreboard styles */
.scoreboard {
  display: flex;
  justify-content: space-between;
  padding: 20px;
  background-color: #C8E1DB;
}

.scoreboard-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.score-label {
  font-size: 16px;
  margin-bottom: 5px;
}

.score-value {
  font-size: 24px;
  font-weight: bold;
}

.score-graphic {
  width: 100px;
  height: 150px;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 10px;
  position: relative;
}

.bar {
  background-color: #7fc1ff;
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  transition: height 0.5s;
}
</style>
