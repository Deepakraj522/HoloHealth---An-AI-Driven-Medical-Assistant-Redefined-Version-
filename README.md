# HoloHealth - An AI-Driven Medical Assistant (Redefined Version)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-green.svg)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

## 🏥 Overview

HoloHealth is a revolutionary AI-driven medical assistant that combines cutting-edge machine learning with intuitive user interface to provide comprehensive healthcare support. This redefined version features enhanced symptom analysis, doctor consultation booking, mental wellness support, and personalized health recommendations.

## ✨ Key Features

### 🔍 **Intelligent Symptom Analysis**
- Advanced AI-powered symptom checker using machine learning models
- Real-time disease prediction based on reported symptoms
- Comprehensive symptom tracking and history
- Integration with medical knowledge databases

### 👨‍⚕️ **Doctor Consultation Platform**
- Smart doctor recommendation based on symptoms and medical conditions
- Comprehensive doctor profiles with specializations and ratings
- Appointment scheduling and management system
- Direct communication channels with healthcare providers

### 🧠 **Mental Wellness Support**
- AI-powered mental health assessment tools
- Personalized wellness recommendations
- Mood tracking and mental health insights
- Access to mental health resources and support

### 📊 **Health Analytics & Insights**
- Interactive health dashboards and visualizations
- Personal health history tracking
- Data-driven health insights and recommendations
- Export capabilities for health reports

### 🔐 **Secure & Privacy-Focused**
- End-to-end encryption for sensitive health data
- HIPAA-compliant data handling
- Secure authentication with Firebase
- User-controlled data privacy settings

## 🏗️ Architecture

### Frontend (React.js)
- **Technology Stack**: React 18.2.0, TailwindCSS, Chart.js
- **Components**:
  - `Home/` - Landing page and dashboard
  - `SymptomAnalysis/` - AI-powered symptom checker
  - `ConsultDoctor/` - Doctor search and consultation
  - `DoctorDetails/` - Detailed doctor profiles
  - `MentalWellness/` - Mental health tools
  - `Navigation/` - App navigation and routing

### Backend (Flask API)
- **Technology Stack**: Flask 3.0.3, Python 3.8+
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **AI Integration**: Google Generative AI, OpenAI API
- **Features**:
  - Disease prediction models
  - Symptom analysis engine
  - Doctor-disease mapping system
  - Health data processing

### Database & Storage
- **Firebase**: Real-time database and authentication
- **Local Storage**: ML models and preprocessed data
- **Data Sources**: Comprehensive medical datasets

## 📁 Project Structure

```
HoloHealth-Organized/
├── 📁 frontend/           # React.js frontend application
│   ├── 📁 public/         # Static assets and HTML template
│   ├── 📁 src/            # React source code
│   │   ├── 📁 Components/ # Reusable React components
│   │   ├── 📁 config/     # Configuration files
│   │   ├── 📁 context/    # React context providers
│   │   ├── 📁 img/        # Image assets
│   │   ├── 📁 styles/     # CSS and styling files
│   │   └── 📁 utils/      # Utility functions
│   ├── package.json       # Frontend dependencies
│   └── tailwind.config.js # TailwindCSS configuration
├── 📁 server/             # Flask backend API
│   ├── 📁 assets/         # ML models and data files
│   │   ├── disease_model.pkl    # Disease prediction model
│   │   ├── encoder.pkl          # Data encoder
│   │   ├── model.pkl           # Main ML model
│   │   └── outcome_model.pkl   # Outcome prediction model
│   ├── app.py             # Main Flask application
│   ├── requirements.txt   # Python dependencies
│   ├── disease_doctor_mapping.json # Doctor specialization mapping
│   └── Disease_to_Doctor_Mapping.csv # Doctor database
├── 📁 dataset/           # Training and reference datasets
│   ├── combined_datasets.csv
│   ├── disease_symptoms_patient_profile.csv
│   └── disease-symptom-description-dataset.csv
├── 📁 notebooks/         # Jupyter notebooks for development
│   ├── Description.ipynb
│   ├── Diases symptom and patient profile.ipynb
│   └── Test combine data.ipynb
└── 📄 README.md          # Project documentation
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v14.0.0 or higher)
- **Python** (3.8 or higher)
- **pip** (Python package manager)
- **Git** (for version control)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Deepakraj522/HoloHealth---An-AI-Driven-Medical-Assistant-Redefined-Version-.git
   cd HoloHealth---An-AI-Driven-Medical-Assistant-Redefined-Version-
   ```

2. **Backend Setup**
   ```bash
   cd server
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Configuration**
   - Copy `server/gemini.json.template` to `server/gemini.json` and add your Google AI API key
   - Copy `server/openai.json.template` to `server/openai.json` and add your OpenAI API key
   - Configure Firebase credentials in `frontend/src/firebase.js`

### Running the Application

1. **Start the Backend Server**
   ```bash
   cd server
   python app.py
   ```
   The API will be available at `http://localhost:5000`

2. **Start the Frontend Development Server**
   ```bash
   cd frontend
   npm start
   ```
   The application will open at `http://localhost:3000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the server directory:

```env
FLASK_APP=app.py
FLASK_ENV=development
GOOGLE_AI_API_KEY=your_google_ai_api_key
OPENAI_API_KEY=your_openai_api_key
```

### Firebase Configuration

Update `frontend/src/firebase.js` with your Firebase project credentials:

```javascript
const firebaseConfig = {
  apiKey: "your-api-key",
  authDomain: "your-auth-domain",
  projectId: "your-project-id",
  storageBucket: "your-storage-bucket",
  messagingSenderId: "your-messaging-sender-id",
  appId: "your-app-id"
};
```

## 🤖 AI & Machine Learning

### Models Used

- **Disease Prediction Model**: Trained on comprehensive symptom-disease datasets
- **Outcome Prediction Model**: Predicts health outcomes based on patient profiles
- **Symptom Encoder**: Processes and normalizes symptom data
- **Google Generative AI**: Powers conversational AI features
- **OpenAI Integration**: Enhances natural language processing

### Dataset Information

- **Combined Datasets**: Aggregated medical data from multiple sources
- **Disease-Symptom Mapping**: Comprehensive symptom-disease relationships
- **Patient Profiles**: Demographic and health profile data
- **Doctor Specialization Database**: Medical practitioner information

## 📱 Features in Detail

### Symptom Analysis
- Input symptoms through intuitive interface
- Real-time AI analysis and disease prediction
- Confidence scores and probability rankings
- Detailed explanations and recommendations

### Doctor Consultation
- AI-powered doctor recommendations
- Filter by specialization, location, and availability
- Comprehensive doctor profiles with reviews
- Appointment booking and management

### Mental Wellness
- Mental health screening tools
- Personalized wellness plans
- Progress tracking and insights
- Resource recommendations

### Health Dashboard
- Personal health overview
- Symptom and health history
- Visual analytics and trends
- Export and sharing capabilities

## 🛠️ Development

### Code Structure

#### Frontend Components
- **Modular Design**: Reusable React components
- **State Management**: Context API for global state
- **Styling**: TailwindCSS for responsive design
- **Charts**: Chart.js for data visualizations

#### Backend Architecture
- **RESTful API**: Clean API endpoints
- **ML Pipeline**: Integrated machine learning models
- **Error Handling**: Comprehensive error management
- **CORS**: Cross-origin resource sharing enabled

### Testing

```bash
# Frontend tests
cd frontend
npm test

# Backend tests
cd server
python -m pytest
```

## 🔒 Security & Privacy

- **Data Encryption**: All sensitive data encrypted in transit and at rest
- **Authentication**: Secure user authentication with Firebase
- **Privacy Controls**: User-controlled data sharing preferences
- **Compliance**: HIPAA-compliant data handling practices
- **Audit Trails**: Comprehensive logging for security monitoring

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Deepak Raj** - Project Lead & Developer
- **Contributors** - Open source community

## 📞 Support

- **Documentation**: [Project Wiki](https://github.com/Deepakraj522/HoloHealth---An-AI-Driven-Medical-Assistant-Redefined-Version-/wiki)
- **Issues**: [GitHub Issues](https://github.com/Deepakraj522/HoloHealth---An-AI-Driven-Medical-Assistant-Redefined-Version-/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Deepakraj522/HoloHealth---An-AI-Driven-Medical-Assistant-Redefined-Version-/discussions)

## 🔮 Roadmap

- [ ] **Mobile Application**: React Native mobile app
- [ ] **Telemedicine Integration**: Video consultation features
- [ ] **Wearable Device Support**: Integration with health monitoring devices
- [ ] **Multi-language Support**: Internationalization and localization
- [ ] **Advanced AI Models**: Enhanced prediction accuracy and capabilities
- [ ] **EHR Integration**: Electronic Health Record system integration

## ⚠️ Disclaimer

HoloHealth is designed to assist with health information and should not replace professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical decisions.

---

<div align="center">
  <strong>Built with ❤️ for better healthcare accessibility</strong>
</div>