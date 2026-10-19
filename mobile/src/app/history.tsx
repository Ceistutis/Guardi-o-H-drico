
import { ScrollView, StyleSheet, Text, useColorScheme, View } from 'react-native';
import { Colors } from '@/constants/theme';

const history = [
  { id: '1', time: '14:30', flow: '0,0 L/min', volume: '18,7 L' },
  { id: '2', time: '14:25', flow: '1,8 L/min', volume: '18,7 L' },
  { id: '3', time: '14:20', flow: '2,4 L/min', volume: '15,2 L' },
  { id: '4', time: '14:15', flow: '0,0 L/min', volume: '12,8 L' },
];

export default function HistoryScreen() {
  const scheme = useColorScheme();
  const c = Colors[scheme === 'dark' ? 'dark' : 'light'];
  return (
    <ScrollView
      style={[styles.container, { backgroundColor: c.background }]}
      contentContainerStyle={styles.content}
    >
      <Text style={[styles.title, { color: c.text }]}>Histórico</Text>
      <Text style={[styles.subtitle, { color: c.textSecondary }]}>
        Leituras recentes de consumo de água.
      </Text>

      <View style={styles.summary}>
        <Text style={[styles.label, { color: c.textSecondary }]}>
          Volume da sessão
        </Text>
        <Text style={styles.value}>18,7 litros</Text>
        <Text style={styles.note}>Dados ilustrativos</Text>
      </View>

      <Text style={[styles.sectionTitle, { color: c.text }]}>
        Últimas leituras
      </Text>

      {history.map((item) => (
        <View
          key={item.id}
          style={[
            styles.row,
            { backgroundColor: c.backgroundElement, borderColor: c.border },
          ]}
        >
          <View style={styles.timeBlock}>
            <Text style={[styles.time, { color: c.text }]}>{item.time}</Text>
            <Text style={[styles.label, { color: c.textSecondary }]}>Hoje</Text>
          </View>
          <View style={styles.reading}>
            <Text style={[styles.label, { color: c.textSecondary }]}>Vazão</Text>
            <Text style={[styles.readingValue, { color: c.text }]}>{item.flow}</Text>
          </View>
          <View style={styles.reading}>
            <Text style={[styles.label, { color: c.textSecondary }]}>Volume</Text>
            <Text style={[styles.readingValue, { color: c.text }]}>{item.volume}</Text>
          </View>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F3F7FC' },
  content: { padding: 22, paddingTop: 30 },
  title: { fontSize: 28, fontWeight: '700' },
  subtitle: { marginTop: 8, marginBottom: 24 },
  summary: { backgroundColor: '#153450', borderRadius: 20, padding: 22, marginBottom: 28 },
  label: { fontSize: 11 },
  value: { color: '#FFFFFF', fontSize: 27, fontWeight: '700', marginTop: 8 },
  note: { color: '#C6D8E8', fontSize: 11, marginTop: 8 },
  sectionTitle: { fontSize: 17, fontWeight: '700', marginBottom: 14 },
  row: { flexDirection: 'row', alignItems: 'center', padding: 14, borderRadius: 14, marginBottom: 10, borderWidth: 1 },
  timeBlock: { width: 58 },
  time: { fontWeight: '700', fontSize: 13 },
  reading: { flex: 1, marginLeft: 8 },
  readingValue: { fontSize: 12, fontWeight: '600', marginTop: 5 },
});
