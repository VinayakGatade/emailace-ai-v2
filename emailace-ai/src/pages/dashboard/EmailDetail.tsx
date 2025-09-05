import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Separator } from "@/components/ui/separator";
import { 
  ArrowLeft, 
  Flame, 
  Clock, 
  CheckCircle, 
  User, 
  Mail, 
  Calendar,
  Phone,
  Building,
  Sparkles,
  Send,
  Save,
  Loader2
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { apiService, Email } from "@/lib/api";

const EmailDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const [aiDraft, setAiDraft] = useState("");
  const [isGeneratingDraft, setIsGeneratingDraft] = useState(false);

  // Fetch email data from API
  const { data: email, isLoading, error } = useQuery({
    queryKey: ['email', id],
    queryFn: () => apiService.getEmailDetail(Number(id)),
    enabled: !!id,
  });

  // Generate AI reply mutation
  const generateReplyMutation = useMutation({
    mutationFn: (customPrompt?: string) => apiService.generateReply(Number(id), customPrompt),
    onSuccess: (data) => {
      setAiDraft(data.draft_reply);
      toast({
        title: "AI Draft Generated",
        description: "Review and edit the suggested response before sending.",
      });
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: "Failed to generate AI reply. Please try again.",
        variant: "destructive",
      });
    },
  });

  // Send reply mutation
  const sendReplyMutation = useMutation({
    mutationFn: () => apiService.sendReply(Number(id)),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['emails'] });
      queryClient.invalidateQueries({ queryKey: ['analytics'] });
      toast({
        title: "Reply Sent",
        description: "Your response has been sent successfully.",
      });
      navigate("/dashboard/inbox");
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: "Failed to send reply. Please try again.",
        variant: "destructive",
      });
    },
  });

  const generateAIDraft = async () => {
    setIsGeneratingDraft(true);
    generateReplyMutation.mutate();
    setIsGeneratingDraft(false);
  };

  const handleSendReply = () => {
    sendReplyMutation.mutate();
  };

  const handleSaveDraft = () => {
    toast({
      title: "Draft Saved",
      description: "Your draft has been saved.",
    });
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin" />
        <span className="ml-2">Loading email...</span>
      </div>
    );
  }

  if (error || !email) {
    return (
      <div className="text-center py-12">
        <div className="text-destructive mb-2">Error loading email</div>
        <div className="text-sm text-muted-foreground">
          {error instanceof Error ? error.message : 'Email not found'}
        </div>
        <Button onClick={() => navigate("/dashboard/inbox")} className="mt-4">
          Back to Inbox
        </Button>
      </div>
    );
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  const getPriorityBadge = (priority: string) => {
    const config = {
      urgent: { variant: "destructive" as const, icon: Flame },
      high: { variant: "destructive" as const, icon: Flame },
      normal: { variant: "default" as const, icon: Clock },
      low: { variant: "secondary" as const, icon: CheckCircle }
    };
    
    const { variant, icon: Icon } = config[priority as keyof typeof config] || config.normal;
    
    return (
      <Badge variant={variant} className="flex items-center space-x-1">
        <Icon className="w-3 h-3" />
        <span className="capitalize">{priority} Priority</span>
      </Badge>
    );
  };

  // Parse entities from JSON string
  const entities = email.entities ? JSON.parse(email.entities) : {};

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button variant="ghost" onClick={() => navigate("/dashboard/inbox")}>
            <ArrowLeft className="w-4 h-4" />
          </Button>
          <div>
            <h1 className="text-2xl font-bold">Email Details</h1>
            <p className="text-muted-foreground">#{id}</p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          {getPriorityBadge(email.priority)}
          <Badge variant={email.status === "resolved" ? "default" : "secondary"}>
            {email.status === "resolved" ? "Resolved" : "Pending"}
          </Badge>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Email Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Email Header */}
          <Card className="gradient-card shadow-medium">
            <CardHeader>
              <div className="flex items-start justify-between">
                                  <div className="space-y-2">
                    <CardTitle className="text-xl">{email.subject}</CardTitle>
                    <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                      <div className="flex items-center space-x-1">
                        <User className="w-4 h-4" />
                        <span>{email.sender.split('@')[0]}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Mail className="w-4 h-4" />
                        <span>{email.sender}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Calendar className="w-4 h-4" />
                        <span>{formatDate(email.date)}</span>
                      </div>
                    </div>
                  </div>
                <Badge 
                  variant={email.sentiment === "positive" ? "default" : 
                           email.sentiment === "negative" ? "destructive" : "secondary"}
                >
                  {email.sentiment} sentiment
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="prose prose-sm max-w-none">
                <pre className="whitespace-pre-wrap font-sans text-sm leading-relaxed">
                  {email.body}
                </pre>
              </div>
            </CardContent>
          </Card>

          {/* AI Response */}
          <Card className="gradient-card shadow-medium">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Sparkles className="w-5 h-5 text-primary" />
                <span>AI Draft Reply</span>
              </CardTitle>
              <CardDescription>
                AI-generated response based on email content and context
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {!aiDraft ? (
                <div className="text-center py-8">
                  <Button 
                    onClick={generateAIDraft} 
                    disabled={isGeneratingDraft}
                    className="gradient-primary text-white"
                  >
                    {isGeneratingDraft ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                        Generating AI Response...
                      </>
                    ) : (
                      <>
                        <Sparkles className="w-4 h-4 mr-2" />
                        Generate AI Reply
                      </>
                    )}
                  </Button>
                </div>
              ) : (
                <>
                  <Textarea
                    value={aiDraft}
                    onChange={(e) => setAiDraft(e.target.value)}
                    className="min-h-64 resize-none"
                    placeholder="AI generated response will appear here..."
                  />
                  <div className="flex justify-end space-x-2">
                    <Button variant="outline" onClick={handleSaveDraft}>
                      <Save className="w-4 h-4 mr-2" />
                      Save Draft
                    </Button>
                    <Button onClick={handleSendReply} className="gradient-primary text-white">
                      <Send className="w-4 h-4 mr-2" />
                      Send Reply
                    </Button>
                  </div>
                </>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Sidebar - Extracted Information */}
        <div className="space-y-6">
          {/* Contact Information */}
          <Card className="gradient-card shadow-medium">
            <CardHeader>
              <CardTitle className="text-lg">Contact Information</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center space-x-3">
                <User className="w-4 h-4 text-muted-foreground" />
                <div>
                  <p className="font-medium">{email.sender.split('@')[0]}</p>
                  <p className="text-sm text-muted-foreground">Customer</p>
                </div>
              </div>
              
              <Separator />
              
              <div className="flex items-center space-x-3">
                <Mail className="w-4 h-4 text-muted-foreground" />
                <span className="text-sm">{email.sender}</span>
              </div>
              
              {entities.phone && (
                <div className="flex items-center space-x-3">
                  <Phone className="w-4 h-4 text-muted-foreground" />
                  <span className="text-sm">{entities.phone[0]}</span>
                </div>
              )}
              
              {entities.email && entities.email.length > 1 && (
                <div className="flex items-center space-x-3">
                  <Building className="w-4 h-4 text-muted-foreground" />
                  <span className="text-sm">{entities.email[1]}</span>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Issue Analysis */}
          <Card className="gradient-card shadow-medium">
            <CardHeader>
              <CardTitle className="text-lg">Issue Analysis</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium text-muted-foreground">Summary</label>
                <p className="text-sm mt-1">{email.summary || "No summary available"}</p>
              </div>
              
              <div>
                <label className="text-sm font-medium text-muted-foreground">Priority</label>
                <p className="text-sm mt-1 capitalize">{email.priority}</p>
              </div>
              
              <div>
                <label className="text-sm font-medium text-muted-foreground">Sentiment</label>
                <p className="text-sm mt-1 capitalize">{email.sentiment}</p>
              </div>
              
              <Separator />
              
              <div>
                <label className="text-sm font-medium text-muted-foreground">Extracted Entities</label>
                <div className="text-sm mt-1">
                  {Object.keys(entities).length > 0 ? (
                    <div className="space-y-1">
                      {Object.entries(entities).map(([key, value]) => (
                        <div key={key}>
                          <span className="font-medium">{key}:</span> {Array.isArray(value) ? value.join(', ') : value}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <span className="text-muted-foreground">No entities extracted</span>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card className="gradient-card shadow-medium">
            <CardHeader>
              <CardTitle className="text-lg">Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <Button variant="outline" size="sm" className="w-full justify-start">
                <CheckCircle className="w-4 h-4 mr-2" />
                Mark as Resolved
              </Button>
              <Button variant="outline" size="sm" className="w-full justify-start">
                <Clock className="w-4 h-4 mr-2" />
                Schedule Follow-up
              </Button>
              <Button variant="outline" size="sm" className="w-full justify-start">
                <User className="w-4 h-4 mr-2" />
                Assign to Team Member
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default EmailDetail;