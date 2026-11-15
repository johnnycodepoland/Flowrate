# Flowrate – mobile app

React Native app built with Expo and Expo Router. See the [main README](../README.md) for the project overview.

## Development

```bash
npm install
npx expo start
```

- Backend address: `API_URL` in `config.js`.
- `npm run start:ts` starts Metro on a Tailscale address (for testing on a phone outside the local network).

## Builds

Production builds are made with EAS, always from this folder:

```bash
eas build -p ios --profile production
eas submit -p ios --latest
```

App Store Connect credentials come from an API key passed through environment variables (`EXPO_ASC_API_KEY_PATH`, `EXPO_ASC_KEY_ID`, `EXPO_ASC_ISSUER_ID`, `EXPO_APPLE_TEAM_ID`). Never commit the key.
