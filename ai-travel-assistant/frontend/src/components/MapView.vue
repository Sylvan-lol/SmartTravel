<template>
  <div class="map-container" ref="mapContainer"></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';

const props = defineProps({
  routeData: {
    type: Object,
    default: null
  }
});

const mapContainer = ref(null);
let map = null;
let polyline = null;
let markers = [];

const loadAMapScript = () => {
  return new Promise((resolve, reject) => {
    if (window.AMap) {
      resolve(window.AMap);
      return;
    }
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = `https://webapi.amap.com/maps?v=2.0&key=816307678b20f6842a8dbcbd80faa20f&callback=initAMap`;
    script.onerror = reject;
    window.initAMap = () => {
      resolve(window.AMap);
    };
    document.head.appendChild(script);
  });
};

const initMap = async () => {
  const AMap = await loadAMapScript();
  map = new AMap.Map(mapContainer.value, {
    zoom: 12,
    center: [116.397428, 39.90923], // 默认北京
    viewMode: '2D'
  });
};

const clearMap = () => {
  if (polyline) {
    map.remove(polyline);
    polyline = null;
  }
  markers.forEach(marker => map.remove(marker));
  markers = [];
};

const drawRoute = (data) => {
  if (!map) return;
  clearMap();

  const AMap = window.AMap;
  const { origin, destination, polyline: polylineStr } = data;

  // 解析 polyline 坐标串（高德返回的是 "x1,y1;x2,y2;..."）
  const path = polylineStr.split(';').map(point => {
    const [lng, lat] = point.split(',');
    return [parseFloat(lng), parseFloat(lat)];
  });

  // 绘制路线
  polyline = new AMap.Polyline({
    path,
    strokeColor: '#3b82f6',
    strokeWeight: 6,
    strokeOpacity: 0.8,
    strokeStyle: 'solid'
  });
  map.add(polyline);

  // 添加起点终点标记
  const startMarker = new AMap.Marker({
    position: [origin.lng, origin.lat],
    title: '起点',
    icon: 'https://webapi.amap.com/theme/v1.3/markers/n/start.png'
  });
  const endMarker = new AMap.Marker({
    position: [destination.lng, destination.lat],
    title: '终点',
    icon: 'https://webapi.amap.com/theme/v1.3/markers/n/end.png'
  });
  markers.push(startMarker, endMarker);
  map.add(markers);

  // 调整视野包含整条路线
  map.setFitView([polyline, startMarker, endMarker]);
};

watch(() => props.routeData, (newData) => {
  if (newData && newData.type === 'route' && newData.polyline) {
    drawRoute(newData);
  }
}, { deep: true });

onMounted(() => {
  initMap();
});
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 300px;
  border-radius: var(--border-radius);
  overflow: hidden;
  margin-top: 12px;
}
</style>