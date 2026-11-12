
import { ScrollView, StyleSheet, Text, useColorScheme, View } from 'react-native';
import { Colors } from '@/constants/theme';

const alerts = [
  {
    id: '1',
    title: 'Nenhum vazamento detectado',
    description: 'O sistema não identificou ocorrências no momento.',
    time: 'Agora',
    severity: 'NORMAL',
  },
];

export default function AlertsScreen() {
  const scheme = useColorScheme();
  const c = Colors[scheme === 'dark' ? 'dark' : 'light'];

  return (
  <ScrollView
    style={[styles.container, { backgroundColor: c.background }]}
    contentContainerStyle={styles.content}
  >
    <Text style={[styles.title, { color: c.text }]}>
      Alertas
    </Text>

    <Text style={[styles.subtitle, { color: c.textSecondary }]}>
      Acompanhe as ocorrências do seu sistema hídrico.
    </Text>

    {alerts.map((alert) => (
      <View
        key={alert.id}
        style={[
          styles.card,
          {
            backgroundColor: c.backgroundElement,
            borderColor: c.border,
          },
        ]}
      >
        <Text style={[styles.badge, { color: c.primary }]}>
          ✓ Sistema normal
        </Text>

        <Text style={[styles.cardTitle, { color: c.text }]}>
          {alert.title}
        </Text>

        <Text style={[styles.description, { color: c.textSecondary }]}>
          {alert.description}
        </Text>

        <Text style={[styles.time, { color: c.textSecondary }]}>
          {alert.time}
        </Text>
      </View>
    ))}
  </ScrollView>
);

}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F3F7FC' },
  content: { padding: 22, paddingTop: 30 },
  title: { fontSize: 28, fontWeight: '700', color: '#153450' },
  subtitle: { color: '#75869A', marginTop: 8, marginBottom: 24, lineHeight: 20 },
  card: { backgroundColor: '#FFFFFF', borderRadius: 18, padding: 18, borderWidth: 1, borderColor: '#E6EDF5' },
  badge: { color: '#16845B', fontWeight: '700', fontSize: 12, marginBottom: 14 },
  cardTitle: { color: '#153450', fontSize: 16, fontWeight: '700' },
  description: { color: '#75869A', fontSize: 13, lineHeight: 20, marginTop: 8 },
  time: { color: '#9AA8B8', fontSize: 11, marginTop: 14 },
});
