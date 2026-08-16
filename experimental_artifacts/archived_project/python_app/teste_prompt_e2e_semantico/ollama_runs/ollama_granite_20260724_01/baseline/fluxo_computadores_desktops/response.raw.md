
```typescript
import { chakraTheme } from 'react-native';
import { createApp } from '@testing-library/react';
import { render, fireEvent } from '@testing-library/react-native';
import { DigitalDownloadsPage } from './DigitalDownloadsPage';

describe('Digital Downloads Page', () => {
  const theme = chakraTheme({
    palette: {
      primary: '#2c3e50',
      secondary: '#ecf0f1',
      text: '#333',
    },
  });

  it('should display the Digital Downloads page when accessed from the Digital downloads category', async () => {
    const { getByText } = render(<DigitalDownloadsPage />);

    expect(getByText('Digital Downloads')).toBeInTheDocument();
  });
});
```