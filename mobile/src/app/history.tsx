
import { ScrollView, StyleSheet, Text, View } from 'react-native';

const history = [
  { id: '1', time: '14:30', flow: '0,0 L/min', volume: '18,7 L' },
  { id: '2', time: '14:25', flow: '1,8 L/min', volume: '18,7 L' },
  { id: '3', time: '14:20', flow: '2,4 L/min', volume: '15,2 L' },
  { id: '4', time: '14:15', flow: '0,0 L/min', volume: '12,8 L' },
];

export default function HistoryScreen() {
  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Histórico</Text>
      <Text style={styles.subtitle}>Leituras recentes de consumo de água.</Text>

      <View style={styles.summary}>
        <Text style={styles.label}>Volume da sessão</Text>
        <Text style={styles.value}>18,7 litros</Text>
        <Text style={styles.note}>Dados ilustrativos</Text>
      </View>

      <Text style={styles.sectionTitle}>Últimas leituras</Text>

      {history.map((item) => (
        <View key={item.id} style={styles.row}>
          <View style={styles.timeBlock}>
            <Text style={styles.time}>{item.time}</Text>
            <Text style={styles.label}>Hoje</Text>
          </View>
          <View style={styles.reading}>
            <Text style={styles.label}>Vazão</Text>
            <Text style={styles.readingValue}>{item.flow}</Text>
          </View>
          <View style={styles.reading}>
            <Text style={styles.label}>Volume</Text>
            <Text style={styles.readingValue}>{item.volume}</Text>
          </View>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F3F7FC' },
  content: { padding: 22, paddingTop: 30 },
  title: { fontSize: 28, fontWeight: '700', color: '#153450' },
  subtitle: { color: '#75869A', marginTop: 8, marginBottom: 24 },
  summary: { backgroundColor: '#153450', borderRadius: 20, padding: 22, marginBottom: 28 },
  label: { color: '#8493A4', fontSize: 11 },
  value: { color: '#FFFFFF', fontSize: 27, fontWeight: '700', marginTop: 8 },
  note: { color: '#C6D8E8', fontSize: 11, marginTop: 8 },
  sectionTitle: { color: '#153450', fontSize: 17, fontWeight: '700', marginBottom: 14 },
  row: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#FFFFFF', padding: 14, borderRadius: 14, marginBottom: 10, borderWidth: 1, borderColor: '#E6EDF5' },
  timeBlock: { width: 58 },
  time: { color: '#153450', fontWeight: '700', fontSize: 13 },
  reading: { flex: 1, marginLeft: 8 },
  readingValue: { color: '#153450', fontSize: 12, fontWeight: '600', marginTop: 5 },
});
