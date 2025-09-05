import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Switch } from "@/components/ui/switch";
import { Textarea } from "@/components/ui/textarea";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { 
  User, 
  Mail, 
  Settings as SettingsIcon, 
  Upload, 
  Save, 
  Bell,
  Shield,
  Database,
  Key,
  Zap
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const Settings = () => {
  const { toast } = useToast();
  const [profileData, setProfileData] = useState({
    name: "John Doe",
    email: "john.doe@example.com",
    role: "Support Manager",
    bio: "Experienced customer support professional specializing in technical issue resolution and team management."
  });

  const [notifications, setNotifications] = useState({
    emailAlerts: true,
    urgentEmails: true,
    dailyReports: false,
    teamUpdates: true
  });

  const [integrations, setIntegrations] = useState({
    gmail: { connected: true, account: "john.doe@gmail.com" },
    outlook: { connected: false, account: "" },
    slack: { connected: true, account: "@johndoe" }
  });

  const handleSaveProfile = () => {
    toast({
      title: "Profile Updated",
      description: "Your profile information has been saved successfully.",
    });
  };

  const handleSaveNotifications = () => {
    toast({
      title: "Notification Settings Updated",
      description: "Your notification preferences have been saved.",
    });
  };

  const handleUploadKnowledgeBase = () => {
    toast({
      title: "Knowledge Base Updated",
      description: "Your knowledge base files have been uploaded successfully.",
    });
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mb-2">Settings</h1>
        <p className="text-muted-foreground">
          Manage your account settings and preferences
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Profile Settings */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="gradient-card shadow-medium">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <User className="w-5 h-5" />
                <span>Profile Information</span>
              </CardTitle>
              <CardDescription>
                Update your personal information and profile details
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center space-x-6">
                <Avatar className="w-20 h-20">
                  <AvatarImage src="/placeholder-avatar.jpg" />
                  <AvatarFallback className="gradient-primary text-white text-lg">
                    JD
                  </AvatarFallback>
                </Avatar>
                <div className="space-y-2">
                  <Button variant="outline" size="sm">
                    <Upload className="w-4 h-4 mr-2" />
                    Change Photo
                  </Button>
                  <p className="text-xs text-muted-foreground">
                    JPG, PNG up to 2MB
                  </p>
                </div>
              </div>

              <Separator />

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Full Name</Label>
                  <Input
                    id="name"
                    value={profileData.name}
                    onChange={(e) => setProfileData({...profileData, name: e.target.value})}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">Email Address</Label>
                  <Input
                    id="email"
                    type="email"
                    value={profileData.email}
                    onChange={(e) => setProfileData({...profileData, email: e.target.value})}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="role">Role</Label>
                <Input
                  id="role"
                  value={profileData.role}
                  onChange={(e) => setProfileData({...profileData, role: e.target.value})}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="bio">Bio</Label>
                <Textarea
                  id="bio"
                  rows={3}
                  value={profileData.bio}
                  onChange={(e) => setProfileData({...profileData, bio: e.target.value})}
                  placeholder="Tell us about yourself..."
                />
              </div>

              <div className="flex justify-end">
                <Button onClick={handleSaveProfile} className="gradient-primary text-white">
                  <Save className="w-4 h-4 mr-2" />
                  Save Changes
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Email Integration */}
          <Card className="gradient-card shadow-medium">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Mail className="w-5 h-5" />
                <span>Email Integration</span>
              </CardTitle>
              <CardDescription>
                Connect your email accounts to sync communications
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {Object.entries(integrations).map(([provider, config]) => (
                <div key={provider} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-accent rounded-lg flex items-center justify-center">
                      <Mail className="w-4 h-4" />
                    </div>
                    <div>
                      <p className="font-medium capitalize">{provider}</p>
                      {config.connected && (
                        <p className="text-sm text-muted-foreground">{config.account}</p>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Badge variant={config.connected ? "default" : "secondary"}>
                      {config.connected ? "Connected" : "Not Connected"}
                    </Badge>
                    <Button variant="outline" size="sm">
                      {config.connected ? "Disconnect" : "Connect"}
                    </Button>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Knowledge Base */}
          <Card className="gradient-card shadow-medium">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Database className="w-5 h-5" />
                <span>Knowledge Base</span>
              </CardTitle>
              <CardDescription>
                Upload documents and resources to improve AI responses
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="border-2 border-dashed border-muted rounded-lg p-8 text-center">
                <Upload className="w-8 h-8 text-muted-foreground mx-auto mb-4" />
                <p className="text-sm text-muted-foreground mb-2">
                  Drop files here or click to upload
                </p>
                <p className="text-xs text-muted-foreground mb-4">
                  PDF, DOC, TXT files up to 10MB each
                </p>
                <Button variant="outline" onClick={handleUploadKnowledgeBase}>
                  Select Files
                </Button>
              </div>
              
              <div className="space-y-2">
                <p className="text-sm font-medium">Uploaded Documents</p>
                <div className="space-y-1">
                  <div className="flex items-center justify-between p-2 bg-muted rounded">
                    <span className="text-sm">support-guidelines.pdf</span>
                    <Badge variant="secondary">Active</Badge>
                  </div>
                  <div className="flex items-center justify-between p-2 bg-muted rounded">
                    <span className="text-sm">product-documentation.docx</span>
                    <Badge variant="secondary">Active</Badge>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar Settings */}
        <div className="space-y-6">
          {/* Notification Settings */}
          <Card className="gradient-card shadow-medium">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Bell className="w-5 h-5" />
                <span>Notifications</span>
              </CardTitle>
              <CardDescription>
                Configure your notification preferences
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium">Email Alerts</p>
                  <p className="text-xs text-muted-foreground">Get notified of new emails</p>
                </div>
                <Switch
                  checked={notifications.emailAlerts}
                  onCheckedChange={(checked) => 
                    setNotifications({...notifications, emailAlerts: checked})
                  }
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium">Urgent Emails</p>
                  <p className="text-xs text-muted-foreground">High priority notifications</p>
                </div>
                <Switch
                  checked={notifications.urgentEmails}
                  onCheckedChange={(checked) => 
                    setNotifications({...notifications, urgentEmails: checked})
                  }
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium">Daily Reports</p>
                  <p className="text-xs text-muted-foreground">Summary at end of day</p>
                </div>
                <Switch
                  checked={notifications.dailyReports}
                  onCheckedChange={(checked) => 
                    setNotifications({...notifications, dailyReports: checked})
                  }
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium">Team Updates</p>
                  <p className="text-xs text-muted-foreground">Collaboration notifications</p>
                </div>
                <Switch
                  checked={notifications.teamUpdates}
                  onCheckedChange={(checked) => 
                    setNotifications({...notifications, teamUpdates: checked})
                  }
                />
              </div>

              <div className="pt-4">
                <Button 
                  onClick={handleSaveNotifications} 
                  size="sm" 
                  className="w-full gradient-primary text-white"
                >
                  Save Preferences
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Security Settings */}
          <Card className="gradient-card shadow-medium">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Shield className="w-5 h-5" />
                <span>Security</span>
              </CardTitle>
              <CardDescription>
                Manage your account security
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Button variant="outline" size="sm" className="w-full justify-start">
                <Key className="w-4 h-4 mr-2" />
                Change Password
              </Button>
              <Button variant="outline" size="sm" className="w-full justify-start">
                <Shield className="w-4 h-4 mr-2" />
                Two-Factor Authentication
              </Button>
              <Button variant="outline" size="sm" className="w-full justify-start">
                <SettingsIcon className="w-4 h-4 mr-2" />
                Privacy Settings
              </Button>
            </CardContent>
          </Card>

          {/* AI Settings */}
          <Card className="gradient-card shadow-medium">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Zap className="w-5 h-5" />
                <span>AI Settings</span>
              </CardTitle>
              <CardDescription>
                Configure AI assistance preferences
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="ai-tone">Response Tone</Label>
                <select className="w-full p-2 border rounded">
                  <option>Professional</option>
                  <option>Friendly</option>
                  <option>Formal</option>
                  <option>Casual</option>
                </select>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="ai-length">Response Length</Label>
                <select className="w-full p-2 border rounded">
                  <option>Concise</option>
                  <option>Detailed</option>
                  <option>Comprehensive</option>
                </select>
              </div>

              <div className="pt-4">
                <Button size="sm" className="w-full gradient-primary text-white">
                  Update AI Settings
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Settings;