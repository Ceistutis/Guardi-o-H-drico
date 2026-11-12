
import { ScrollView, StyleSheet, Text, useColorScheme, View } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { Colors } from '@/constants/theme';

const device = {
  id: 'guardiao-001',
  online: true,
  flowRate: 0,
  sessionVolume: 18.7,
  valveState: 'Aberta',
  waterDetected: false,
};

export default function HomeScreen() {
  const scheme = useColorScheme();
  const isDark = scheme === 'dark';
  const c = Colors[isDark ? 'dark' : 'light'];

  const hasLeak = device.waterDetected;

  return (
    <View
      style={[
        styles.container,
        isDark && { backgroundColor: c.background },
      ]}
    >
      <StatusBar style={isDark ? 'light' : 'dark'} />

      <ScrollView
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.header}>
          <View
            style={[
              styles.logo,
              isDark && { backgroundColor: c.backgroundSelected },
            ]}
          >
            <Text style={styles.logoText}>💧</Text>
          </View>

          <View style={styles.headerInfo}>
            <Text style={[styles.title, isDark && { color: c.text }]}>
              Guardião Hídrico
            </Text>
            <Text
              style={[
                styles.subtitle,
                isDark && { color: c.textSecondary },
              ]}
            >
              Monitoramento inteligente
            </Text>
          </View>

          <Text style={[styles.bell, isDark && { color: c.text }]}>♧</Text>
        </View>

        <Text style={[styles.sectionTitle, isDark && { color: c.text }]}>
          Visão geral
        </Text>

        <View
          style={[
            styles.statusCard,
            isDark && {
              backgroundColor: c.backgroundElement,
              borderColor: c.border,
            },
          ]}
        >
          <View style={styles.statusRow}>
            <View
              style={[
                styles.dot,
                { backgroundColor: device.online ? '#16A36A' : '#DC5353' },
              ]}
            />

            <Text
              style={[
                styles.connectionText,
                isDark && { color: c.success },
              ]}
            >
              {device.online ? 'Dispositivo conectado' : 'Dispositivo offline'}
            </Text>

            <View
              style={[
                styles.onlineBadge,
                isDark && { backgroundColor: c.backgroundSelected },
              ]}
            >
              <Text
                style={[
                  styles.onlineText,
                  isDark && { color: c.primary },
                ]}
              >
                {device.online ? 'ONLINE' : 'OFFLINE'}
              </Text>
            </View>
          </View>

          <Text
            style={[
              styles.deviceId,
              isDark && { color: c.textSecondary },
            ]}
          >
            ID: {device.id}
          </Text>

          <View
            style={[
              styles.divider,
              isDark && { backgroundColor: c.border },
            ]}
          />

          <Text
            style={[
              styles.statusTitle,
              isDark && { color: c.text },
            ]}
          >
            {hasLeak
              ? 'Possível vazamento detectado'
              : 'Sistema operando normalmente'}
          </Text>

          <Text
            style={[
              styles.description,
              isDark && { color: c.textSecondary },
            ]}
          >
            {hasLeak
              ? 'Verifique os sensores e a instalação.'
              : 'Nenhum sinal de água detectado pelo sensor.'}
          </Text>
        </View>

        <Text style={[styles.sectionTitle, isDark && { color: c.text }]}>
          Consumo de água
        </Text>

        <View style={styles.metrics}>
          <View
            style={[
              styles.metricCard,
              isDark && {
                backgroundColor: c.backgroundElement,
                borderColor: c.border,
              },
            ]}
          >
            <Text style={styles.metricIcon}>〰️</Text>
            <Text
              style={[
                styles.metricLabel,
                isDark && { color: c.textSecondary },
              ]}
            >
              Vazão atual
            </Text>
            <Text
              style={[
                styles.metricValue,
                isDark && { color: c.text },
              ]}
            >
              {device.flowRate.toLocaleString('pt-BR', {
                minimumFractionDigits: 1,
                maximumFractionDigits: 1,
              })}
            </Text>
            <Text
              style={[
                styles.metricUnit,
                isDark && { color: c.textSecondary },
              ]}
            >
              litros/minuto
            </Text>
          </View>

          <View
            style={[
              styles.metricCard,
              isDark && {
                backgroundColor: c.backgroundElement,
                borderColor: c.border,
              },
            ]}
          >
            <Text style={styles.metricIcon}>💧</Text>
            <Text
              style={[
                styles.metricLabel,
                isDark && { color: c.textSecondary },
              ]}
            >
              Volume da sessão
            </Text>
            <Text
              style={[
                styles.metricValue,
                isDark && { color: c.text },
              ]}
            >
              {device.sessionVolume.toLocaleString('pt-BR')}
            </Text>
            <Text
              style={[
                styles.metricUnit,
                isDark && { color: c.textSecondary },
              ]}
            >
              litros
            </Text>
          </View>
        </View>

        <Text style={[styles.sectionTitle, isDark && { color: c.text }]}>
          Controle da água
        </Text>

        <View
          style={[
            styles.valveCard,
            isDark && {
              backgroundColor: c.backgroundElement,
              borderColor: c.border,
            },
          ]}
        >
          <View
            style={[
              styles.valveIcon,
              isDark && { backgroundColor: c.backgroundSelected },
            ]}
          >
            <Text style={styles.valveEmoji}>🚰</Text>
          </View>

          <View style={styles.valveInfo}>
            <Text
              style={[
                styles.valveTitle,
                isDark && { color: c.text },
              ]}
            >
              Válvula principal
            </Text>
            <Text
              style={[
                styles.valveDescription,
                isDark && { color: c.textSecondary },
              ]}
            >
              Estado reportado pelo dispositivo
            </Text>
          </View>

          <View
            style={[
              styles.valveBadge,
              isDark && { backgroundColor: c.backgroundSelected },
            ]}
          >
            <Text
              style={[
                styles.valveBadgeText,
                isDark && { color: c.success },
              ]}
            >
              {device.valveState}
            </Text>
          </View>
        </View>

        <Text
          style={[
            styles.footer,
            isDark && { color: c.textSecondary },
          ]}
        >
          Dados simulados para demonstração
        </Text>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F3F7FC',
  },
  content: {
    padding: 22,
    paddingTop: 28,
    paddingBottom: 36,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 30,
  },
  logo: {
    width: 48,
    height: 48,
    borderRadius: 16,
    backgroundColor: '#DCEEFF',
    alignItems: 'center',
    justifyContent: 'center',
  },
  logoText: {
    fontSize: 26,
  },
  headerInfo: {
    flex: 1,
    marginLeft: 12,
  },
  title: {
    color: '#153450',
    fontSize: 20,
    fontWeight: '700',
  },
  subtitle: {
    color: '#75869A',
    fontSize: 12,
    marginTop: 4,
  },
  bell: {
    fontSize: 25,
    color: '#153450',
  },
  sectionTitle: {
    color: '#153450',
    fontSize: 17,
    fontWeight: '700',
    marginBottom: 13,
    marginTop: 8,
  },
  statusCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 20,
    padding: 18,
    marginBottom: 25,
    borderWidth: 1,
    borderColor: '#E6EDF5',
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
    flexWrap: 'wrap',
    gap: 7,
  },
  dot: {
    width: 9,
    height: 9,
    borderRadius: 5,
  },
  connectionText: {
    color: '#245A48',
    fontSize: 12,
    fontWeight: '600',
    flex: 1,
  },
  onlineBadge: {
    backgroundColor: '#DDF6E9',
    borderRadius: 20,
    paddingHorizontal: 9,
    paddingVertical: 5,
  },
  onlineText: {
    color: '#16845B',
    fontSize: 10,
    fontWeight: '700',
  },
  deviceId: {
    color: '#8493A4',
    fontSize: 12,
    marginTop: 12,
  },
  divider: {
    height: 1,
    backgroundColor: '#EDF1F6',
    marginVertical: 15,
  },
  statusTitle: {
    color: '#153450',
    fontSize: 16,
    fontWeight: '700',
  },
  description: {
    color: '#75869A',
    fontSize: 12,
    lineHeight: 19,
    marginTop: 7,
  },
  metrics: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 25,
  },
  metricCard: {
    flex: 1,
    backgroundColor: '#FFFFFF',
    borderRadius: 20,
    padding: 15,
    borderWidth: 1,
    borderColor: '#E6EDF5',
  },
  metricIcon: {
    fontSize: 23,
    marginBottom: 14,
  },
  metricLabel: {
    color: '#75869A',
    fontSize: 12,
    minHeight: 32,
  },
  metricValue: {
    color: '#153450',
    fontSize: 27,
    fontWeight: '700',
    marginTop: 5,
  },
  metricUnit: {
    color: '#8493A4',
    fontSize: 10,
    marginTop: 5,
  },
  valveCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    borderRadius: 20,
    padding: 15,
    borderWidth: 1,
    borderColor: '#E6EDF5',
  },
  valveIcon: {
    width: 44,
    height: 44,
    borderRadius: 14,
    backgroundColor: '#EAF4FF',
    alignItems: 'center',
    justifyContent: 'center',
  },
  valveEmoji: {
    fontSize: 23,
  },
  valveInfo: {
    flex: 1,
    marginLeft: 10,
  },
  valveTitle: {
    color: '#153450',
    fontWeight: '700',
    fontSize: 13,
  },
  valveDescription: {
    color: '#8493A4',
    fontSize: 10,
    marginTop: 5,
  },
  valveBadge: {
    backgroundColor: '#DDF6E9',
    paddingHorizontal: 10,
    paddingVertical: 7,
    borderRadius: 20,
  },
  valveBadgeText: {
    color: '#16845B',
    fontSize: 12,
    fontWeight: '700',
  },
  footer: {
    color: '#9AA8B8',
    fontSize: 11,
    textAlign: 'center',
    marginTop: 24,
  },
});
