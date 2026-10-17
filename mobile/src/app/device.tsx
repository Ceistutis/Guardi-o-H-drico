
import { ScrollView, StyleSheet, Text, View } from 'react-native';

export default function DeviceScreen() {
  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Dispositivo</Text>
      <Text style={styles.subtitle}>Informações do Guardião Hídrico.</Text>

      <View style={styles.card}>
        <View style={styles.icon}>
          <Text style={styles.emoji}>📡</Text>
        </View>

        <Text style={styles.deviceName}>Guardião Hídrico</Text>
        <Text style={styles.deviceId}>guardiao-001</Text>

        <View style={styles.badge}>
          <Text style={styles.badgeText}>● Online (simulado)</Text>
        </View>
      </View>

      <Text style={styles.sectionTitle}>Informações técnicas</Text>

      <View style={styles.infoCard}>
        <Text style={styles.label}>Microcontrolador</Text>
        <Text style={styles.value}>ESP32</Text>
        <View style={styles.divider} />

        <Text style={styles.label}>Sensor de vazão</Text>
        <Text style={styles.value}>YF-S201 (planejado)</Text>
        <View style={styles.divider} />

        <Text style={styles.label}>Estado reportado da válvula</Text>
        <Text style={styles.value}>Aberta</Text>
        <View style={styles.divider} />

        <Text style={styles.label}>Última comunicação</Text>
        <Text style={styles.value}>Dado de demonstração</Text>
      </View>

      <Text style={styles.disclaimer}>
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
  card: { backgroundColor: '#FFFFFF', borderRadius: 20, padding: 24, alignItems: 'center', borderWidth: 1, borderColor: '#E6EDF5' },
  icon: { width: 68, height: 68, borderRadius: 22, backgroundColor: '#DCEEFF', alignItems: 'center', justifyContent: 'center', marginBottom: 15 },
  emoji: { fontSize: 32 },
  deviceName: { color: '#153450', fontSize: 18, fontWeight: '700' },
  deviceId: { color: '#8493A4', marginTop: 6, fontSize: 12 },
  badge: { backgroundColor: '#DDF6E9', paddingHorizontal: 13, paddingVertical: 8, borderRadius: 20, marginTop: 16 },
  badgeText: { color: '#16845B', fontWeight: '600', fontSize: 12 },
  sectionTitle: { color: '#153450', fontSize: 17, fontWeight: '700', marginTop: 28, marginBottom: 14 },
  infoCard: { backgroundColor: '#FFFFFF', borderRadius: 18, padding: 18, borderWidth: 1, borderColor: '#E6EDF5' },
  label: { color: '#8493A4', fontSize: 12 },
  value: { color: '#153450', fontSize: 14, fontWeight: '600', marginTop: 6 },
  divider: { height: 1, backgroundColor: '#EDF1F6', marginVertical: 15 },
  disclaimer: { color: '#8493A4', fontSize: 11, textAlign: 'center', marginTop: 20 },
});
