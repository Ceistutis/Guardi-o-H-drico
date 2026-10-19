
import { ScrollView, StyleSheet, Text, useColorScheme, View } from 'react-native';
import { Colors } from '@/constants/theme';

export default function DeviceScreen() {
  const scheme = useColorScheme();
  const c = Colors[scheme === 'dark' ? 'dark' : 'light'];

  return (
    <ScrollView
      style={[styles.container, { backgroundColor: c.background }]}
      contentContainerStyle={styles.content}
    >
      <Text style={[styles.title, { color: c.text }]}>Dispositivo</Text>
      <Text style={[styles.subtitle, { color: c.textSecondary }]}>
        Informações do Guardião Hídrico.
      </Text>

      <View style={[styles.card, { backgroundColor: c.backgroundElement, borderColor: c.border }]}>
        <View style={[styles.icon, { backgroundColor: c.backgroundSelected }]}>
          <Text style={styles.emoji}>📡</Text>
        </View>

        <Text style={[styles.deviceName, { color: c.text }]}>Guardião Hídrico</Text>
        <Text style={[styles.deviceId, { color: c.textSecondary }]}>guardiao-001</Text>

        <View style={[styles.badge, { backgroundColor: c.backgroundSelected }]}>
          <Text style={[styles.badgeText, { color: c.success }]}>
            ● Online (simulado)
          </Text>
        </View>
      </View>

      <Text style={[styles.sectionTitle, { color: c.text }]}>
        Informações técnicas
      </Text>

      <View style={[styles.infoCard, { backgroundColor: c.backgroundElement, borderColor: c.border }]}>
        <Text style={[styles.label, { color: c.textSecondary }]}>Microcontrolador</Text>
        <Text style={[styles.value, { color: c.text }]}>ESP32</Text>
        <View style={[styles.divider, { backgroundColor: c.border }]} />

        <Text style={[styles.label, { color: c.textSecondary }]}>Sensor de vazão</Text>
        <Text style={[styles.value, { color: c.text }]}>YF-S201 (planejado)</Text>
        <View style={[styles.divider, { backgroundColor: c.border }]} />

        <Text style={[styles.label, { color: c.textSecondary }]}>Estado reportado da válvula</Text>
        <Text style={[styles.value, { color: c.text }]}>Aberta</Text>
        <View style={[styles.divider, { backgroundColor: c.border }]} />

        <Text style={[styles.label, { color: c.textSecondary }]}>Última comunicação</Text>
        <Text style={[styles.value, { color: c.text }]}>Dado de demonstração</Text>
      </View>

      <Text style={[styles.disclaimer, { color: c.textSecondary }]}>
        Nenhum comando físico é enviado nesta versão.
      </Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F3F7FC' },
  content: { padding: 22, paddingTop: 30 },
  title: { fontSize: 28, fontWeight: '700', color: '#153450' },
  subtitle: { color: '#75869A', marginTop: 8, marginBottom: 24 },
  card: { borderRadius: 20, padding: 24, alignItems: 'center', borderWidth: 1 },
  icon: { width: 68, height: 68, borderRadius: 22, alignItems: 'center', justifyContent: 'center', marginBottom: 15 },
  emoji: { fontSize: 32 },
  deviceName: { fontSize: 18, fontWeight: '700' },
  deviceId: { marginTop: 6, fontSize: 12 },
  badge: { paddingHorizontal: 13, paddingVertical: 8, borderRadius: 20, marginTop: 16 },
  badgeText: { fontWeight: '600', fontSize: 12 },
  sectionTitle: { fontSize: 17, fontWeight: '700', marginTop: 28, marginBottom: 14 },
  infoCard: { borderRadius: 18, padding: 18, borderWidth: 1 },
  label: { fontSize: 12 },
  value: { fontSize: 14, fontWeight: '600', marginTop: 6 },
  divider: { height: 1, marginVertical: 15 },
  disclaimer: { fontSize: 11, textAlign: 'center', marginTop: 20 },
});
