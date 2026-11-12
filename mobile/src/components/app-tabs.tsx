
import { NativeTabs } from 'expo-router/native-tabs';
import { useColorScheme } from 'react-native';

import { Colors } from '@/constants/theme';

export default function AppTabs() {
  const scheme = useColorScheme();
  const colors = Colors[scheme === 'dark' ? 'dark' : 'light'];

  return (
    <NativeTabs
      backgroundColor={colors.background}
      indicatorColor={colors.backgroundElement}
      labelStyle={{
        default: {
          color: colors.textSecondary,
        },
        selected: {
          color: colors.primary,
        },
      }}
    >
      <NativeTabs.Trigger name="index">
        <NativeTabs.Trigger.Label>Início</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon
          sf="house.fill"
          md="home"
        />
      </NativeTabs.Trigger>

      <NativeTabs.Trigger name="alerts">
        <NativeTabs.Trigger.Label>Alertas</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon
          sf="bell.fill"
          md="notifications"
        />
      </NativeTabs.Trigger>

      <NativeTabs.Trigger name="history">
        <NativeTabs.Trigger.Label>Histórico</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon
          sf="chart.bar.fill"
          md="bar_chart"
        />
      </NativeTabs.Trigger>

      <NativeTabs.Trigger name="device">
        <NativeTabs.Trigger.Label>Dispositivo</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon
          sf="sensor.fill"
          md="sensors"
        />
      </NativeTabs.Trigger>
    </NativeTabs>
  );
}
